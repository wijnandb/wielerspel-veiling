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

    

def get_rider_on_auction():
    """
    Slightly more complicated. Get the first item of AuctionOrder (teamcaptain)
    Use that TeamCaptain to get the first Unsold rider from ToBeAuctioned from that TeamCaptain
    """
    teamcaptain = TeamCaptain.objects.first().team_captain
    next = ToBeAuctioned.objects.filter(team_captain=teamcaptain).filter(sold=False).first()
    next_rider = next.rider

    return teamcaptain, next_rider


class AuctionView(TemplateView):
    """
    This is the page where the actual auctioning takes place.
    We want to refresh all data with Javascript, so initial view
    shouldn't provide any data
    """
    template_name = 'veiling/veiling.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        team_captain, rider_on_auction = get_rider_on_auction()
        context['ploegleiders'] = TeamCaptain.objects.all()
        context['team_captain'] = team_captain.get_full_name()
        context['rider'] = rider_on_auction
        context['max_allowed'] = TeamCaptain.objects.get(team_captain=self.request.user)
        return context


@login_required
def biddings(request):
    """ 
        Get all biddings. 
        As long as the team_captain who propeses the rider to be auctioned hasn't place a bid,
        no-one else can.
        After he places the opening-bid, we check the auto-biddings from ToBeAuctioned and decide 
        which team_captain holds the highest bid and how high it is. 
        The rules: 
        - teamcaptain with highest bid gets the bid.
        - the amount is one higher than the second highest bid
        - if there is more than one team_captain with the highest bid, a randomizer decides who gets the bid
        - before allowing a bid, we check whether it can be placed (does TeamCaptain hold enough points)
    """
    results = []

    team_captain, rider_on_auction = get_rider_on_auction()
    #print(team_captain, rider_on_auction)

    # if this rider exists in the Joker table, we want to get the user it belongs to and the value
    # this either True or False. If False, we only nee
    if Joker.objects.filter(rider=rider_on_auction).exists():
        # we want to know if it's this user that has the joker
        # we now check in page
        joker_info = Joker.objects.get(rider=rider_on_auction)
        #joker_tc = joker_info.team_captain
        joker_tc_name = joker_info.team_captain.first_name
        #joker_value = joker_info.value
        #joker_info = "joker"
    else:
        joker_info = None

    # aantal biedingen tonen
    # bij nieuwe renner ter bieding, openingsbod tonen
    biddings = Bid.objects.order_by('-created')[:10]
    print(biddings)
    new_biddings = Bid.objects.filter(rider_id=rider_on_auction)

    # What if I check whether the first bidding is by the Team_captain who proposed the rider
    # and delete /ignore everything else until that is the case 
    if biddings:
        #print("we have biddings!")
        for bidding in biddings:
            results.append({'name': bidding.team_captain.get_full_name,
                        'amount': bidding.amount,
                        'rider': bidding.rider.name})
            print(results)
        # here it goes wrong: there are biddings, but not for this rider

        if new_biddings:
            #print("we have new biddings!")
            highestbid = new_biddings.order_by('-amount').first()
            highest = highestbid.amount
            winner = highestbid.team_captain
            timestamp = highestbid.created
            nu=datetime.now()
            time_remaining = round(20 - (nu-timestamp).total_seconds())
            #print(verschil)
            #timestamp = naturaltime(highestbid.created)
            # WIP something below here is an object and by such not JSON serializable
            return JsonResponse(status=200, data={'status': _('success'),
                                                'data': results,
                                                'on_auction': rider_on_auction.name,
                                                #'joker_tc':joker_tc,
                                                #'joker_tc_name':joker_tc_name,
                                                #'joker_value':joker_value,
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
                                                #'joker_tc':joker_tc,
                                                #'joker_tc_name':joker_tc_name,
                                                #'joker_value':joker_value,
                                                'joker_info': joker_info,
                                                'timer': 20})

    else:
        return JsonResponse(status=200, data={'status': _('succes'),
                                            'highest': 'Wacht op openingsbod',
                                            'winner': '',
                                            'on_auction': rider_on_auction.name,
                                            'joker_info': joker_info})

"""
@login_required
def bidding(request):
    print("enter bidding")
    if request.method == 'POST':
        user = request.user
        form = BidForm(request.POST)
        if not form.is_valid():
            # Return form error if return false
            return JsonResponse(status=400, data={'status': _('error'),
                                                  'msg': form.errors})
        teamcaptain, rider = get_rider_on_auction()
        amount = form.cleaned_data['amount']
        print(f"User is {user}, tc is {teamcaptain}")
        print(user==teamcaptain)
        if no_opening_bid(rider):
            print(f"Waiting for first bid by { teamcaptain }")
            if user == teamcaptain:
                print(" user is temacaptain who proposed rider")
            # teamcaptain who proposed the rider, so accept his bid
                place_opening_bid(teamcaptain, rider, amount)
                return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
            else:
                print("wachten op eerste bod")
                raise Exception("Waiting for first bid by proposing team_captain")
        else:
            try:
                get_highest_bid = biddings[0].amount

                if get_highest_bid == form.cleaned_data['amount']:
                    # only allow if user has a Joker
                    if check_joker(user, rider):
                        # you can allow the bid
                        new_bidding = Bid(rider=rider, team_captain=user, amount=form.cleaned_data['amount'])
                    else:
                        #disallow, no joker and equal bid
                        print("disallow it")
                        raise Exception("Bod moet hoger zijn dan huidige hoogste bod. Geen joker.")
                elif get_highest_bid > form.cleaned_data['amount']:
                    # Raise exception once the new bid is lower than current bid highest bid
                    raise Exception("Bod moet hoger zijn dan huidige hoogste bod")

                else:
                    # new bid is higher than highest bid
                    new_bidding = Bid(rider=rider, team_captain=user, amount=form.cleaned_data['amount'])
                
                # enough = TeamCaptain.objects.filter(user=user)
                if TeamCaptain.objects.filter(user=user)[0].max_allowed_bid() >= form.cleaned_data['amount']:
                    new_bidding.save()
                    
                else:
                    raise Exception("Not enough points left to make that bid")

                print("Reached end of bidding, send success message")
                return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})

            except Exception as err:
                return JsonResponse(status=400, data={'status': _('error'), 'msg': str(err) })
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})
"""

@login_required
def bidding(request):
    """  Bid gets received form form.
    Check """
    if request.method == 'POST':
        user = request.user
        form = BidForm(request.POST)
        teamcaptain, rider = get_rider_on_auction()
        if form.is_valid():
            amount = form.cleaned_data['amount']
            print(f"Amount in cleaned_data is {amount}")
            if opening_bid_exists:
                if process_bid(user, rider, amount):
                    return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
                else:
                    print("No bid placed")
            elif user == teamcaptain:
                print(f"{user} is {teamcaptain}")
                place_opening_bid(teamcaptain, rider, amount)
                return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
            else:
                print(f"Wacht op openingbod van {teamcaptain}")
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})      

def joker_bid(request):
    pass

def process_bid(user, rider, amount):
    b= Bid(team_captain=user, rider=rider, amount=amount)
    b.save()
    print("placed bid! Check in admin")
    return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})

def opening_bid_exists(rider):
    """
    check if there already is an opening bid. If so, return true.
    Else, check if it's the temacaptain who proposed the rider who wants to place
    a bid.
    """
    if Bid.objects.filter(rider=rider).exists():
        return True
    else:
        return False


def place_opening_bid(teamcaptain, rider, amount):
    """ If opening bid is to high, adjust it to the allowed amount """
    print("entering place_opening_bid")
    amount = allowed_to_make_bid(teamcaptain, amount)
    print(amount)
    b = Bid(rider=rider, team_captain=teamcaptain, amount=amount)
    b.save()
    print("Openingbid is placed, check if it is in the table")


def allowed_to_make_bid(teamcaptain, amount):
    """
    If the amount is higher than allowed, change it to the proper amount.
    Need to check if the potentially lower amount is still high enough to allow
    """
    max_allowed_bid = TeamCaptain.objects.get(team_captain=teamcaptain).max_allowed_bid()
    print(max_allowed_bid)
    if  max_allowed_bid < amount:
        amount = max_allowed_bid
    return amount


def check_joker(user, rider):
    return Joker.objects.filter(rider=rider).filter(team_captain=user).exists()


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
def get_highest():
    """ 
        Get highest bid.
        The logic here dictates that the highest bid is one higher than the second highest bid,
        unless of course when second_highest == highest_bid. So it seems we want to get both the highest 
        and the second highest bid, check if highest > second_highest and then set 
        highest = second_highest + 1 and return this amount
    """
    results = []
    highest = 0
    team_captain, rider_on_auction = get_rider_on_auction()
    biddings = Bid.objects.filter(rider=rider_on_auction).order_by('-amount', 'created')
    if len(biddings) > 1:
        highest_bid = biddings[0]
        second_highest = biddings[1]
        if highest_bid.amount > second_highest.amount:
            highest = second_highest.amount+1
        highest = highest_bid.amount
        results.append({'name': highest_bid.team_captain,
                        'amount': highest,
                        'date': naturaltime(highest_bid.created)})
    else:
        results.append({'name': team_captain,
                        'amount': "Wacht op openingsbod van {teamcaptain}",
                        })
    return JsonResponse(status=200, data={'status': _('success'),
                                          'data': results})


