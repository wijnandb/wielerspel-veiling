from django.contrib.auth.models import User
from django.db import models
from results.models import Rider


class Bid(models.Model):
    """
    The bidding. Who bids how much for whom?
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()  # Thinking it should be a DecimalField
    # @aladelekan: Only integers allowed, whole points as biddings. That's the rules,  
    # otherwise you are totally right. Please remove once you have read this.
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.username, self.rider.name, self.amount)


class TeamCaptain(models.Model):
    """ 
    Information about the TeamCaptains: how many riders have they bought,
    how much points do they have left, what is max. bid, how many riders 
    do they still need to buy?
    """
    team_size = models.IntegerField(default=0)
    amount_left = models.IntegerField(default=100)
    riders_needed = models.IntegerField(default=9)
    max_allowed_bid = models.IntegerField(default=92)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "%s heeft %s renners (nog %s nodig). Max. toegestaan bod: %s. Punten over: %s" %(self.user, self.team_size, self.riders_needed, self.max_allowed_bid, self.amount_left)

    class Meta:
        ordering = ['-amount_left', '-user']



class ToBeAuctioned(models.Model):
    """
    The wishlist for each Teamcaptain. A rider can be on the wishlist of 
    multiple TeamCaptains. Once a rider is auctioned, it is removed from 
    everyone's wishlist.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s wil %s aanbieden voor %s" %(self.team_captain, self.rider, self.amount)


class Joker(models.Model):
    """
    TeamCaptains can have a "Joker" placed on three riders they have had in
    previos year(s). This allows them to buy that Rider for a lower amont than 
    the other TeamCaptains. A Joker with a value of 0 allows them to buy the
    rider for the highest amount the other TeamCaptains have bidded.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "%s heeft een %s joker op %s" %(self.team_captain, self.value, self.rider.name)


class VirtualTeam(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ploegleider = models.ForeignKey(TeamCaptain, on_delete=models.CASCADE)
    editie = models.PositiveIntegerField(default=2021)
    price = models.IntegerField(default=0)
    punten = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    unique_together = [['rider', 'editie']]

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Sold riders'

    def __str__(self):
        return "%s - %s -%s" %(self.rider, self.price, self.ploegleider)


class Verkocht(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ploegleider = models.ForeignKey(TeamCaptain, on_delete=models.CASCADE)
    editie = models.PositiveIntegerField(default=2021)
    price = models.IntegerField(default=0)
    punten = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    unique_together = [['rider', 'editie']]

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('verkochterenners-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Verkochte renners'

    def __str__(self):
        return str(self.rider)
