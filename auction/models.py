from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Bid(models.Model):
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey('results.Rider', on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()  # Thinking it should be a DecimalField
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.username, self.rider.name, self.amount)


class TeamCaptainStatus(models.Model):
    team_size = models.IntegerField(default=0)
    amount_left = models.IntegerField(default=100)
    riders_needed = models.IntegerField(default=9)
    max_allowed_bid = models.IntegerField(default=92)
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s riders (need %s more) max bid: %s points left: %s" %(self.team_captain.username, self.team_size, self.riders_needed, self.max_allowed_bid, self.amount_left)
