from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from django.db.models import UniqueConstraint

#from auction.models import TeamCaptain


class Rider(models.Model):
    """
    The riders, the cyclists
    """
    id = models.PositiveIntegerField(primary_key=True)
    rank = models.IntegerField(null=True, blank=True)
    prev = models.IntegerField(null=True, blank=True)
    cqriderid = models.PositiveIntegerField(unique=True)
    ucicode = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=3, blank=True, null=True)
    nationality = models.CharField(max_length=3, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    cqpoints = models.IntegerField(null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def image_link(self):
        link = str(self.id)
        #print(f"eerste link = { link }")
        digits = len(link)
        while digits < 6:
            link = "0"+link
            #print(link)
            digits = len(link)

        return link+".jpg"
    
        
    def current_age(self):
        if self.ucicode:
            if len(self.ucicode) < 11:
                try:
                    birthdate = self.ucicode
                    born = datetime.datetime.strptime(birthdate, "%d/%m/%Y").date()
                    #print(born)
                    today = datetime.date.today()
                    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                    return age
                except:
                    return "Onbekende geboortedatum"
            else:
                try:
                    day = self.ucicode[-2:]
                    month = self.ucicode[-4:-2]
                    year = self.ucicode[-8:-4]
                    birthdate = day+month+year
                    born = datetime.datetime.strptime(birthdate, "%d%m%Y").date()
                    today = datetime.date.today()
                    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                    return age
                except:
                    return "Onbekende geboortedatum"

        else:
            return "Onbekende geboortedatum"

    class Meta:
        ordering = ['rank']

    def get_absolute_url(self):
        return reverse('rider-detail', kwargs={'pk': self.pk})
    
    @property
    def calculated_points(self):
        return CalculatedPoints.objects.get(rider=self.id, editie=2022).points
    
    @property
    def calculated_jpp(self):
       return CalculatedPoints.objects.get(rider=self.id, editie=2022).jpp
    
    @property
    def spelpunten(self):
        from auction.models import VirtualTeam
        try:
            return VirtualTeam.objects.get(rider=self.id, editie=2023).punten
        except:
            return "*"

    @property
    def points2021(self):
        return CalculatedPoints.objects.get(editie=2021, rider_id=self.id).points

    @property
    def points2020(self):
        return CalculatedPoints.objects.get(editie=2020, rider_id=self.id).points

    @property
    def points2019(self):
        return CalculatedPoints.objects.get(editie=2019, rider_id=self.id).points

    @property
    def points2018(self):
        return CalculatedPoints.objects.get(editie=2018, rider_id=self.id).points

    @property
    def jpp2021(self):
        return CalculatedPoints.objects.get(editie=2021, rider_id=self.id).jpp

    @property
    def jpp2020(self):
        return CalculatedPoints.objects.get(editie=2020, rider_id=self.id).jpp

    @property
    def jpp2019(self):
        return CalculatedPoints.objects.get(editie=2019, rider_id=self.id).jpp

    @property
    def jpp2018(self):
        return CalculatedPoints.objects.get(editie=2018, rider_id=self.id).jpp

    @property
    def average(self):
        return (self.calculated_points+self.points2021+self.points2020)/3
    
    @property
    def averagejpp(self):
        return (self.calculated_jpp+self.jpp2021+self.jpp2020)/3

     
    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of the model."""
    #     return reverse('rider-detail', kwargs={'year': self.year, 'riderid': str(self.cqriderid)})


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    category_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'UCI-category'
        verbose_name_plural = 'UCI-Categorieën'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('category-detail', args=[str(self.pk)])


class RacePoints(models.Model):
    editie = models.PositiveIntegerField(default=2022)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ranking = models.IntegerField()
    points = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Punten per race'
        verbose_name_plural = 'Punten per race'
        unique_together = ("editie", "category", "ranking")
        ordering = ('ranking',)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('racepoints-detail', args=[str(self.pk)])

    def __str__(self):
        return str(self.ranking)


class Race(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    editie = models.PositiveIntegerField(default=2022)
    cqraceid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=150)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-startdate']
  
    def get_absolute_url(self):
        return reverse('race-detail', kwargs={'pk': self.pk})


class Uitslag(models.Model):
    """ 
    We will import results from CQRanking, which means that races and riders will
    be linked through the CQRanking ID's 
    """
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    rank = models.IntegerField()  # we'll fix the "leader" differently. Use '0' as a rank
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('race-detail', args=[str(self.race)])

    class Meta:
        verbose_name_plural = 'Uitslagen'
        unique_together = ("race", "rank")
        ordering = ("-race__startdate", "rank")
    
    @property
    def points(self):
        #return RacePoints.objects.filter(ranking=self.rank).filter(category=1)
        return RacePoints.objects.get(ranking=self.rank, category__race=self.race)
    
    @property
    def teamcaptain(self):
        """ Let's think about performance. It will look up a team_captain for every result there is.
        That is a lot of queries. 
        """
        from auction.models import VirtualTeam
        return VirtualTeam.objects.get(rider=self.rider, editie=self.race.editie)


class CalculatedPoints(models.Model):
    """
    Calculate points per rider for each edition and store it here, so we can compare
    with the "official" results.
    """
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    editie = models.PositiveIntegerField(default=2022)
    points = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    jpp = models.IntegerField(default=0)

    UniqueConstraint(fields=['rider', 'editie'], name='points_per_edition')

    def __str__(self):
        return str(self.rider.name)

    # def points2022(self):
    #     return 


    class Meta:
        verbose_name_plural = "Calculated points"
        unique_together = ("rider", "editie")

    


class Teams(models.Model):
    """
    Show a page with the cyclingteams, so we can clickthrough and show riders per team.
    The teams are now linked to riders by a three-letter abbreviation and it chnages evrey year, no 
    solution (yet) to keep track of teams.
    """
    pass