from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Rider(models.Model):
    rank = models.IntegerField(null=True, blank=True)
    prev = models.IntegerField(null=True, blank=True)
    cqriderid = models.IntegerField(unique=True)
    ucicode = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=3, blank=True, null=True)
    nationality = models.CharField(max_length=3, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    cqpoints = models.IntegerField(null=True, blank=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['rank']


class Category(models.Model):
    category = models.CharField(unique=True, max_length=20)
    category_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'UCI-category'
        verbose_name_plural = 'UCI-Categorieën'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('category-detail', args=[str(self.id)])


class RacePoints(models.Model):
    editie = models.PositiveIntegerField(default=2020)
    category = models.ForeignKey(Category, to_field='category', on_delete=models.CASCADE)
    ranking = models.CharField(max_length=50)
    points = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Punten per race'
        verbose_name_plural = 'Punten per race'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('racepoints-detail', args=[str(self.id)])

    def __str__(self):
        return self.category, self.ranking


class Race(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, to_field='category', on_delete=models.SET_NULL, null=True)
    cqraceid = models.IntegerField(default=0, unique=True)
    country = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-startdate']


class Uitslag(models.Model):
    race = models.ForeignKey(Race, to_field='cqraceid', on_delete=models.SET_NULL, null=True)
    rank = models.CharField(max_length=20)  # because we have "leader" as rank as well
    rider = models.ForeignKey(Rider, to_field='cqriderid', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('race-detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'Uitslagen'

