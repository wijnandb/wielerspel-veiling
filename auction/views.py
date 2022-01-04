from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from datetime import datetime
import time
from django.db.models import Count, Sum
from django.contrib.humanize.templatetags.humanize import naturaltime
from auction.forms import LoginForm, RegistrationForm, BidForm, ChangeSortForm
from auction.models import Bid, Joker, TeamCaptain, ToBeAuctioned, VirtualTeam
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


class ToBeAuctionedListView(generic.ListView):
    model = ToBeAuctioned
    context_object_name = 'renners'
    
    def get_queryset(self, **kwargs):
        return ToBeAuctioned.objects.filter(team_captain=self.request.user).filter(sold=False)


@require_POST
@login_required
def AddRiderToBeAuctioned(request):
    rider = Rider.objects.get(id=request.POST.get('riderID'))
    amount = request.POST.get('amount')
    team_captain = request.user
    #print(f"adding {rider} to list of {team_captain} with value {amount}")
    try:
        tba = ToBeAuctioned.objects.get(team_captain=team_captain, rider=rider)
        tba.amount = amount
        tba.save()
        return JsonResponse({'status':'updated existing'})
    except:
        tba = ToBeAuctioned(team_captain=team_captain, rider=rider, amount=amount)
        tba.save()
        #print(f"Added {rider} for {team_captain} for ${amount}")
        return JsonResponse({"status": "Added a new rider"})


@require_POST
@login_required
def RemoveRiderToBeAuctioned(request):
    rider = Rider.objects.get(id=request.POST.get('riderID'))
    team_captain = request.user
    try:
        tba = ToBeAuctioned.objects.get(team_captain=team_captain, rider=rider)
        tba.delete()
        return JsonResponse({'status':'removed rider'})
    except:
        print("Rider not on wishlist")


@require_POST
@login_required
def SaveOrderingToBeAuctioned(request):
    """
    Drag and drop form changes the order of riders to be auctioned
    """
    form = ChangeSortForm(request.POST)

    if form.is_valid():
        ordered_ids = form.cleaned_data["ordering"].split(',')

        print(ordered_ids)
        #with transaction.atomic():
        current_order = 1
        for lookup_id in ordered_ids:
            rider = ToBeAuctioned.objects.get(id=lookup_id)
            rider.order = current_order
            rider.save()
            current_order += 1

    response = {'msg':'Submitted Successfully',
                'url':'geheimelijst',
                'created':True}
    return redirect('/geheimelijst/')


class TeamCaptainListView(generic.ListView):
    model = TeamCaptain
    context_object_name = 'team_captains'
    template_name = 'auction/auctionorder.html'


class JokerListView(ListView):
    model = Joker

    def get_queryset(self, **kwargs):
        return Joker.objects.filter(rider__sold=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['geheimelijst'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context
