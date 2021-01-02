from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from auction.forms import LoginForm, RegistrationForm, BidForm
from auction.models import Bid, TeamCaptain, ToBeAuctioned
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
        return reverse('register')

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
        rider_id = self.kwargs['rider_id']
        context['rider_id'] = rider_id
        context['rider'] = Rider.objects.get(id=rider_id)
        context['ploegleiders'] = TeamCaptain.objects.all()
        return context


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
            Fetch all bidding for a team captain and check each
            credit if less than the new credit
            """
            biddings = Bid.objects.filter(rider_id=form.cleaned_data['rider'], team_captain=user)
            if len(biddings) < 1:
                """ Raise exception if queryset return 0 """
                raise Bid.DoesNotExist

            get_last_bid = biddings.latest('created')

            if get_last_bid.amount >= form.cleaned_data['amount']:
                """ Raise exception once the new bid is lower than current bid highest bid """
                raise Exception("New bid must not be lower than or equal to the current bid")

            new_bidding = Bid(rider_id=form.cleaned_data['rider'], team_captain=user, amount=form.cleaned_data['amount'])
        except Bid.DoesNotExist:
            new_bidding = Bid(rider_id=form.cleaned_data['rider'], team_captain=user, amount=form.cleaned_data['amount'])
        except Exception as err:
            return JsonResponse(status=400, data={'status': _('error'), 'msg': str(err) })

        new_bidding.save()

        return JsonResponse(status=200, data={'status': _('success'), 'msg': _('Bid successfully')})
    else:
        return JsonResponse(status=405, data={'status': _('error'), 'msg': _('Method not allowed')})


@login_required
def get_current(request):
    """ Get current highest bid for a user """
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id, team_captain=request.user)
    obj = biddings.latest("created")
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
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id)
    obj = biddings.recent("-created")
    return JsonResponse(status=200, data={'status': _('success'),
                                          'msg': obj.amount})

@login_required
def biddings(request):
    """ 
        Get all biddings. 
        Actually, we don't want to get all biddings really. 
        We want to get the highest biddings. Based on the second highest bid, we 
        determine how high the highest bid should be.
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
                        'date': highest_bid.created})
        results.append({'name': second_highest.team_captain.username,
                        'amount': second_highest.amount,
                        'date': second_highest.created})
    else:
        for bidding in biddings:
            results.append({'name': bidding.team_captain.username,
                        'amount': bidding.amount,
                        'date': bidding.created})

    return JsonResponse(status=200, data={'status': _('success'),
                                          'data': results,
                                          'highest': highest})


class ToBeAuctionedListView(generic.ListView):
    model = ToBeAuctioned

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['objects'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context
