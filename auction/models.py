from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Bid(models.Model):
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_captain')
    rider = models.ForeignKey('results.Rider', on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()  # Thinking it should be a DecimalField
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.username, self.rider.name, self.amount)