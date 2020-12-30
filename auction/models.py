from django.contrib.auth.models import User
from django.db import models


class Bid(models.Model):
    """
    The bidding. Who bids how much for whom?
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey('results.Rider', on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()  # Thinking it should be a DecimalField
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.username, self.rider.name, self.amount)


class TeamCaptain(models.Model):
    """ 
    Information about the TeamCaptains, how many riders have they bought,
    how much points left, what is max. bid
    """
    team_size = models.IntegerField(default=0)
    amount_left = models.IntegerField(default=100)
    riders_needed = models.IntegerField(default=9)
    max_allowed_bid = models.IntegerField(default=92)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "%s heeft %s renners (nog %s nodig). Max toegestaan bod: %s. Punten over: %s" %(self.user, self.team_size, self.riders_needed, self.max_allowed_bid, self.amount_left)

class ToBeAuctioned(models.Model):
    """
    The wishlist for each Teamcaptain. A rider can be on the wishlist of 
    multiple TeamCaptains. Once a rider is auctioned, it is removed from 
    everyone's wishlist.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey('results.Rider', on_delete=models.CASCADE)
    amount = models.IntegerField()  # Thinking it should be a DecimalField
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s wil %s aanbieden voor %s" %(self.team_captain, self.rider, self.amount)