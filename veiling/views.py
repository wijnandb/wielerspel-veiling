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
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from django.contrib.humanize.templatetags.humanize import naturaltime
from auction.forms import LoginForm, RegistrationForm, BidForm
from auction.models import Bid, TeamCaptain, ToBeAuctioned, VirtualTeam, Joker
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
    try:
        next_rider = ToBeAuctioned.objects.filter(sold=False).order_by('created').first().rider
    except:
        next_rider = None

    return next_rider


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
    #rider_name = rider_on_auction.name
    #rider_id = rider_on_auction.id

    # if this rider exists in the Joker table, we want to get the user it belongs to and the value
    # this either True or False. If False, we only nee
    if Joker.objects.filter(rider=rider_on_auction.id).exists():
        # we want to know if it's this user that has the joker
        # we now check in page
        joker_info = Joker.objects.get(rider=rider_on_auction.id)
        joker_tc_id = joker_info.team_captain.id
        joker_tc_name = joker_info.team_captain.first_name
        joker_value = joker_info.value
        joker_info = "joker"
    else:
        joker_tc_id = 0
        joker_tc_name = ''
        joker_value = ''
        joker_info = 'Geen joker'

    # aantal biedingen tonen
    # bij nieuwe renner ter bieding, openingsbod tonen
    biddings = Bid.objects.filter(rider_id=rider_on_auction.id).order_by('-created')[:20]
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
                                                'on_auction': rider_on_auction.name,
                                                'joker_tc_id':joker_tc_id,
                                                'joker_tc_name':joker_tc_name,
                                                'joker_value':joker_value,
                                                'joker_info': joker_info,
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
                                                'on_auction': rider_on_auction.name,
                                                'joker_tc_id':joker_tc_id,
                                                'joker_tc_name':joker_tc_name,
                                                'joker_value':joker_value,
                                                'joker_info': joker_info,
                                                'timer': 20})

    else:
        return JsonResponse(status=200, data={'status': _('succes'),
                                            'highest': 'Begin veiling!',
                                            'winner': '',
                                            'on_auction': rider_on_auction.name,
                                            'joker_info': joker_info})


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
            It cannot be lower than the current highest bid
            Except when it is a Joke bid. Let's start accepting equal biddings
            """
            # get the rider that is on auction
            rider = get_rider_on_auction()
            rider_id = rider.id
            biddings = Bid.objects.filter(rider_id=rider_id).order_by('-amount')
            if len(biddings) < 1:
                """ first bid, so highest_bid = 0 """
                get_highest_bid = 0
            else:
                get_highest_bid = biddings[0].amount

            if get_highest_bid == form.cleaned_data['amount']:
                # only allow if user has a Joker
                if check_joker(user, rider_id):
                    # you can allow the bid
                    new_bidding = Bid(rider_id=rider_id, team_captain=user, amount=form.cleaned_data['amount'])
                else:
                    #disallow, no joker and equal bid
                    print("disallow it")
                    raise Exception("Bod moet hoger zijn dan huidige hoogste bod. Geen joker.")
            elif get_highest_bid > form.cleaned_data['amount']:
                """ Raise exception once the new bid is lower than current bid highest bid """
                raise Exception("Bod moet hoger zijn dan huidige hoogste bod")

            else:
                # new bid is higher than highest bid
                new_bidding = Bid(rider_id=rider_id, team_captain=user, amount=form.cleaned_data['amount'])
            
            enough = TeamCaptain.objects.filter(user=user)
            if TeamCaptain.objects.filter(user=user)[0].max_allowed_bid() >= form.cleaned_data['amount']:
                new_bidding.save()
            else:
                raise Exception("Not enough points left to make that bid")

            return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})

        except Exception as err:
            return JsonResponse(status=400, data={'status': _('error'), 'msg': str(err) })
            #pass
        """ Check if user is allowed to make this bid, if he has enough points remaining """

        
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})

def process_bid():
    pass

def check_high_enough_bid():
    pass


def allowed_to_make_bid():
    pass

def check_joker(user, rider_id):
    return Joker.objects.filter(rider=rider_id).filter(team_captain=user).exists()


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
            highest = second_highest.amount+1
        highest = highest_bid.amount
        results.append({'name': highest_bid.team_captain.username,
                        'amount': highest,
                        'date': naturaltime(highest_bid.created)})
    return JsonResponse(status=200, data={'status': _('success'),
                                          'data': results})


class ToBeAuctionedListView(generic.ListView):
    model = ToBeAuctioned

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['renners'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context
