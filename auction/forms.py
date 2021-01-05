from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import TextInput
from auction.models import VirtualTeam, ToBeAuctioned


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'text', 'id': 'username',
                                                                      'placeholder': 'Enter Username'}))
    password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'password', 'id': 'password',
                                                                      'placeholder': 'Enter Password'}))


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'f-name',
                                           'placeholder': 'Enter first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'l_name',
                                          'placeholder': 'Enter last name'}),
            'username': TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'username',
                                         'placeholder': 'Enter username'}),
            'email': TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'email',
                                      'placeholder': 'Enter email'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password', 'id': 'password',
                                         'placeholder': 'Enter password'})
        }

    def clean(self):
        clean_data = self.cleaned_data
        # check if email or username already exists
        user = User.objects.filter(Q(username=clean_data['username']) | Q(email=clean_data['email']))
        if len(user) != 0:
            raise forms.ValidationError('Username or email already exists. Please try another one')

        return clean_data


class BidForm(forms.Form):
    rider = forms.IntegerField()
    amount = forms.IntegerField()


class AddToBeAuctioned(forms.Form):
    model = ToBeAuctioned
