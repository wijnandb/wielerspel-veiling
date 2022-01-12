from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, UniqueConstraint
from results.models import Rider


class TeamCaptain(models.Model):
    """ 
    Information about the TeamCaptains: how many riders have they bought,
    how much points do they have left, what is max. bid, how many riders 
    do they still need to buy?
    """
    team_captain = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    order = models.IntegerField(default=0)
    riders_proposed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.team_captain.get_full_name())

    @property
    def team_size(self):
        from auction.models import VirtualTeam
        team_size = VirtualTeam.objects.filter(ploegleider=self.team_captain, editie=2022).count()
        return team_size
    
    def riders_needed(self):
        if self.team_size < 9:
            return (9-self.team_size)
        else:
            return self.team_size()

    def amount_left(self):
        from auction.models import VirtualTeam
        spend = VirtualTeam.objects.filter(ploegleider=self.team_captain, editie=2022).aggregate(Sum('price'))
        if spend['price__sum'] == None:
            spend['price__sum']=0    
        amount_left = 100 - spend['price__sum']
        return amount_left

    @property
    def max_allowed_bid(self):
        if self.team_size > 8:
            return self.amount_left()
        else:
            return self.amount_left()-self.riders_needed()+1

    def riders_for_auction(self):
        """
        How many riders unsold riders does a temacaptain have on his list?
        If this is low or even zero, warn him to add a rider to his list
        """
        from auction.models import ToBeAuctioned
        return ToBeAuctioned.objects.filter(team_captain=self.team_captain).filter(sold=False).count()

    def next_rider_on_auction(self):
        from auction.models import ToBeAuctioned
        try:
            return ToBeAuctioned.objects.filter(team_captain=self.team_captain).filter(sold=False)[0].rider
        except:
            return "geen"

    class Meta:
        ordering = ['riders_proposed', 'order']


class Bid(models.Model):
    """
    The bidding. Who bids how much for whom?
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.get_full_name(), self.rider, self.amount)


class ToBeAuctioned(models.Model):
    """
    The wishlist for each Teamcaptain. A rider can be on the wishlist of 
    multiple TeamCaptains. Once a rider is auctioned, it is removed from 
    everyone's wishlist (by setting sold =True).
    """
    order = models.IntegerField(blank=False, default=100_000)
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'modified']
        unique_together = ("team_captain", "rider")

    def __str__(self):
        return "%s biedt %s aan voor %s" %(self.team_captain.get_full_name(), self.rider.name, self.amount)


class Joker(models.Model):
    """
    TeamCaptains can have a "Joker" placed on three riders they have had in
    previous year(s). This allows them to buy that Rider for a lower amount than 
    the other TeamCaptains. A Joker with a value of 0 allows them to buy the
    rider for the highest amount the other TeamCaptains have bidded.
    A Joker with a negative value gets them the discount of that value.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "%s %s %s" %(self.team_captain.get_full_name(), self.value, self.rider.name)
    
    class Meta:
        ordering = ['team_captain']


class VirtualTeam(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ploegleider = models.ForeignKey(User, on_delete=models.CASCADE)
    editie = models.PositiveIntegerField(default=2022)
    price = models.IntegerField(default=0)
    punten = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    UniqueConstraint(fields=['rider', 'editie'], name='verkochte_renner') 

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Virtual Teams'

    def __str__(self):
        return "%s - %s - %s" %(self.rider, self.price, self.ploegleider.get_full_name())
