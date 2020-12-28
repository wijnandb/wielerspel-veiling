from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from auction.forms import LoginForm, RegistrationForm
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




