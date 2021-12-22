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
    name = models.CharField(max_length=30, default='naam invoeren')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


    @property
    def team_size(self):
        from auction.models import VirtualTeam
        team_size = VirtualTeam.objects.filter(ploegleider=self.user).count()
        return team_size
    
    def riders_needed(self):
        if self.team_size < 9:
            return (9-self.team_size)
        else:
            return self.team_size()

    def amount_left(self):
        from auction.models import VirtualTeam
        spend = VirtualTeam.objects.filter(ploegleider=self.user).aggregate(Sum('price'))
        if spend['price__sum'] == None:
            spend['price__sum']=0    
        amount_left = 100 - spend['price__sum']
        return amount_left

    def max_allowed_bid(self):
        if self.team_size > 8:
            return self.amount_left()
        else:
            return self.amount_left()-self.riders_needed()+1
    
    class Meta:
        ordering = ['name']


class Bid(models.Model):
    """
    The bidding. Who bids how much for whom?
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='rider')
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s - %s" %(self.team_captain.username, self.rider.name, self.amount)



class ToBeAuctioned(models.Model):
    """
    The wishlist for each Teamcaptain. A rider can be on the wishlist of 
    multiple TeamCaptains. Once a rider is auctioned, it is removed from 
    everyone's wishlist.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "%s biedt %s aan voor %s" %(self.team_captain, self.rider.name, self.amount)


class AuctionOrder(models.Model):
    """
    We need to determine the order in which riders are being auctioned.
    The TeamCaptains take turns proposing a rider to be auctioned.
    After each auctioned rider, the order has to be changed: number 1
    teamcaptain shifts to last order (count(teamcaptains)+1) and then each
    order goes -1: order = order -1
    Once a TeamCaptain doesn't have anymore points to spend, he gets 
    taken of the list.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField()


class Joker(models.Model):
    """
    TeamCaptains can have a "Joker" placed on three riders they have had in
    previous year(s). This allows them to buy that Rider for a lower amount than 
    the other TeamCaptains. A Joker with a value of 0 allows them to buy the
    rider for the highest amount the other TeamCaptains have bidded.
    """
    team_captain = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return "%s %s %s" %(self.team_captain.first_name, self.value, self.rider.name)
    
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
        return "%s - %s - %s" %(self.rider, self.price, self.ploegleider)
