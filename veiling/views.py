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
from veiling.forms import BidForm


class AuctionView(TemplateView):
    """
    This is the page where the actual auctioning takes place.
    We want to refresh all data with Javascript, so initial view
    shouldn't provide any data
    """
    template_name = 'veiling/veiling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Now I want to get the rider to be auctioned from the model ToBeAuctioned
        #rider = Rider.objects.filter(sold=False).first()
        #rider_id = rider.id
        # this is how we used to do it:
        #rider_id = self.kwargs['rider_id']
        #context['rider_id'] = rider_id
        #context['rider'] = Rider.objects.get(id=rider_id)
        context['ploegleiders'] = TeamCaptain.objects.all()
        return context

def get_rider_on_auction():
    return Rider.objects.filter(sold=False).order_by('rank').first()


@login_required
def biddings(request):
    """ 
        Get all biddings. 
    """
    results = []
    """
    This is now where we get the rider that is on Auction.
    Transfer it to a different function so we can more easily change it?
    """
    rider_on_auction = get_rider_on_auction()
    rider_name = rider_on_auction.name
    rider_id = rider_on_auction.id

    # if this rider exists in the Joker table, we want to get the user it belongs to and the value
    # 404 get? 

    #aantal biedingen tonen
    biddings = Bid.objects.order_by('-created')[:10]
    new_biddings = Bid.objects.filter(rider_id=rider_on_auction.id)

    if biddings:
        #print("we have biddings!")
        for bidding in biddings:
            results.append({'name': bidding.team_captain.username,
                        'amount': bidding.amount,
                        'rider': bidding.rider.name})
        # here it goes wrong: there are biddings, but not for this rider
    
        if new_biddings:
            #print("we have new biddings!")
            highestbid = new_biddings.order_by('-amount').first()
            highest = highestbid.amount
            winner = highestbid.team_captain.username
            timestamp = highestbid.created
            nu=datetime.now()
            time_remaining = round(20 - (nu-timestamp).total_seconds())
            #print(verschil)
            #timestamp = naturaltime(highestbid.created)

            return JsonResponse(status=200, data={'status': _('success'),
                                                'data': results,
                                                'on_auction': rider_name,
                                                'highest': highest,
                                                'winner': winner,
                                                'timer': time_remaining})
        else:
            # this is the case where we already have a sold rider
            # but no new biddings
            # we could show some info on the sold rider
            return JsonResponse(status=200, data={'status': _('succes'),
                                                'data': results,
                                                'highest': '0',
                                                'winner': 'plaats een bod',
                                                'on_auction': rider_name,
                                                'timer': 20})

    else:
        return JsonResponse(status=200, data={'status': _('succes'),
                                            'highest': 'Begin veiling!',
                                            'winner': 'Plaats het eerste bod!',
                                            'on_auction': rider_name})


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
            # get the rider that is on auction
            rider = get_rider_on_auction()
            rider_id = rider.id
            biddings = Bid.objects.filter(rider_id=rider_id).order_by('-amount')
            if len(biddings) < 1:
                """ Raise exception if queryset return 0 """
                raise Bid.DoesNotExist
            else:
                get_highest_bid = biddings[0]

                if get_highest_bid.amount >= form.cleaned_data['amount']:
                    """ Raise exception once the new bid is lower than current bid highest bid """
                    raise Exception("Bod moet hoger zijn dan huidige hoogste bod")
                
            new_bidding = Bid(rider_id=rider_id, team_captain=user, amount=form.cleaned_data['amount'])
        except Bid.DoesNotExist:
            print('Eerste bod op deze renner')
            new_bidding = Bid(rider_id=rider_id, team_captain=user, amount=form.cleaned_data['amount'])
        except Exception as err:
            return JsonResponse(status=400, data={'status': _('error'), 'msg': str(err) })
            #pass
        """ Check if user is allowed to make this bid, if he has enough points remaining """
        enough = TeamCaptain.objects.filter(user=user)
        if TeamCaptain.objects.filter(user=user)[0].max_allowed_bid() >= form.cleaned_data['amount']:
            new_bidding.save()
        else:
            pass

        return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})


@login_required
def get_current(request):
    """ Get current highest bid for a user """
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id).order_by('-amount')
    if len(biddings) > 0:
        amount = biddings[0].amount
    else:
        # if there are no biddings yet, put in a bidding of 0 to avoid errormessage
        amount = 0
    return JsonResponse(status=200, data={'status': _('success'),
                                          'msg': amount})


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
