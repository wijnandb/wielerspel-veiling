from django import forms


class BidForm(forms.Form):
    amount = forms.IntegerField()