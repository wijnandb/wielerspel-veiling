from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from datetime import datetime
import time
from django.db.models import Count, Sum
from django.contrib.humanize.templatetags.humanize import naturaltime
from auction.forms import LoginForm, RegistrationForm, BidForm
from auction.models import Bid, TeamCaptain, ToBeAuctioned, VirtualTeam
from results.models import Rider

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, "No account found. Please check login credentials and try again")
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('results:index')


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('auction:register')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)


class AuctionView(TemplateView):
    """
    This is the page where the actual auctioning takes place.
    Stuff that is missing:
    - get rider to be auctioned from AuctionOrder (could be a list, not necessarily a table)
    - add Joker button
    - show loggedin Teamcaptains
    """
    template_name = 'auction/auction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Now I want to get the rider to be auctioned from the model ToBeAuctioned
        rider = Rider.objects.filter(sold=False).first()
        rider_id = rider.id
        # this is how we used to do it:
        #rider_id = self.kwargs['rider_id']
        context['rider_id'] = rider_id
        context['rider'] = Rider.objects.get(id=rider_id)
        context['ploegleiders'] = TeamCaptain.objects.all()
        return context


@login_required
def biddings(request):
    """ 
        Get all biddings. 
    """
    results = []
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id).order_by('-created')

    if biddings:
        for bidding in biddings:
            results.append({'name': bidding.team_captain.username,
                        'amount': bidding.amount,
                        'date': naturaltime(bidding.created)})

        highestbid = Bid.objects.filter(rider_id=rider_id).order_by('-amount')[0]
        highest = highestbid.amount
        winner = highestbid.team_captain.username
        timestamp = naturaltime(biddings[0].created)

        return JsonResponse(status=200, data={'status': _('success'),
                                            'data': results,
                                            'highest': highest,
                                            'winner': winner,
                                            'latest': timestamp})
    else:
        return JsonResponse(status=200, data={'status': _('succes'),
                                            'highest': 'Nog geen biedingen',
                                            'winner': 'plaats een bod'})


@login_required
def bidding(request):
    if request.method == 'POST':
        user = request.user
        form = BidForm(request.POST)
        if not form.is_valid():
            # Return form error if return false
            return JsonResponse(status=400, data={'status': _('error'),
                                                  'msg': form.errors})
        try:
            """
            Here we have to check if the bid is allowed. 
            It cannot be lower or equal to the current highest bid
            """
            biddings = Bid.objects.filter(rider_id=form.cleaned_data['rider']).order_by('-amount')
            if len(biddings) < 1:
                """ Raise exception if queryset return 0 """
                raise Bid.DoesNotExist
            else:
                get_highest_bid = biddings[0]

                if get_highest_bid.amount >= form.cleaned_data['amount']:
                    """ Raise exception once the new bid is lower than current bid highest bid """
                    raise Exception("Bod moet hoger zijn dan huidige hoogste bod")

            new_bidding = Bid(rider_id=form.cleaned_data['rider'], team_captain=user, amount=form.cleaned_data['amount'])
        except Bid.DoesNotExist:
            new_bidding = Bid(rider_id=form.cleaned_data['rider'], team_captain=user, amount=form.cleaned_data['amount'])
        except Exception as err:
            #return JsonResponse(status=400, data={'status': _('error'), 'msg': str(err) })
            pass

        new_bidding.save()

        return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})


@login_required
def get_current(request):
    """ Get current highest bid for a user """
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id).order_by('-amount')
    if biddings:
        obj = biddings[0]
    else:
        # if there are no biddings yet, put in a bidding of 0 to avoid errormessage
        obj.amount = 0
    return JsonResponse(status=200, data={'status': _('success'),
                                          'msg': obj.amount})


@login_required
def get_highest(request):
    """ 
        Get highest bid.
        The logic here dictates that the highest bid is one higher than the second highest bid,
        unless of course when second_highest == highest_bid. So it seems we want to get both the highest 
        and the second highest bid, check if highest > second_highest and then set 
        highest = second_highest + 1 and return this amount
    """
    results = []
    highest = 1
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id).order_by('-amount', 'created')
    if len(biddings) > 1:
        highest_bid = biddings[0]
        second_highest = biddings[1]
        if highest_bid.amount > second_highest.amount:
            highest_bid.amount = second_highest.amount+1
        highest = highest_bid.amount
        results.append({'name': highest_bid.team_captain.username,
                        'amount': highest_bid.amount,
                        'date': naturaltime(highest_bid.created)})
    return JsonResponse(status=200, data={'status': _('success'),
                                          'data': results})


class ToBeAuctionedListView(generic.ListView):
    model = ToBeAuctioned

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['renners'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context

def GetWinner():
    """
    This is the function that gets the latest rider that was bid on, finds the
    highest bid on that rider and sells that rider to the highest bidder.
    We could (and maybe should) add:
    - check if rider is already sold
    - latest bid is at least 10 seconds old

    Have to do:
    - set rider to "sold"
    
    """
    # first, check what the latest bid was
    latest = Bid.objects.order_by('-created')
    # get the rider that was bidded on
    # could be improved by checking on latest unsold rider
    if latest:
        Timestamp = latest[0].created
        #print(Timestamp)
        #print(type(Timestamp))
        nu=datetime.now()
        #print(nu)
        #print(type(nu))
        #print((nu-Timestamp).total_seconds())
        verschil = ((nu-Timestamp).total_seconds())
        #print(verschil)
        # I want to know if the latest bid has been
        # at least 10 seconds ago. If that is the case, the
        # bidding should be closed and the rider goes to the
        # highest bidder. 

        if verschil > 10:
            latestrider = latest[0].rider
            print(latestrider.id)
            if not VirtualTeam.objects.filter(rider=latestrider, editie=2021).exists():
                # print(latestrider)
                # get the highest bid on that rider
                # extra sort on created, so we get the Joker bid (same value, later entry) 
                highest = Bid.objects.filter(rider=latestrider).order_by('-amount', '-created')
                # this was the winning bid
                winner=highest[0]
                #print(winner)
                print(winner.rider, winner.team_captain, winner.amount)
                renner = VirtualTeam()
                renner.rider = winner.rider
                renner.ploegleider = winner.team_captain
                renner.price = winner.amount
                renner.editie = 2021
                renner.save()

                sold_rider = Rider.objects.get(id=winner.rider_id)
                sold_rider.sold = True
                sold_rider.save()

            else:
                print(f'{latestrider} is al verkocht')
        else:
            print("Nog bezig met bieden")
    else:
        print(f"Nog geen biedingen aanwezig")
