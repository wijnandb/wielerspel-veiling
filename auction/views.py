from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.utils.translation import gettext as _
from auction.forms import LoginForm, RegistrationForm, BidForm
from auction.models import Bid


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
        return reverse('index')


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('register')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)


class AuctionListView(TemplateView):
    template_name = 'auction/auctions.html'


class AuctionView(TemplateView):
    template_name = 'auction/auction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rider_id'] = self.kwargs['rider_id']
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
            print(get_last_bid.amount)
            print(form.cleaned_data['amount'])

            if get_last_bid.amount > form.cleaned_data['amount']:
                """ Raise exception once the new bid is lower than current bid for same user """
                raise Exception("New bid must not be lower than the current bid")

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
    """ Get current bid number for a user """
    rider_id = request.GET.get('rider_id')
    biddings = Bid.objects.filter(rider_id=rider_id)
    obj = biddings.latest("created")
    return JsonResponse(status=200, data={'status': _('success'),
                                          'msg': obj.amount})


