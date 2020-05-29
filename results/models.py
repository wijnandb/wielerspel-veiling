from django.db import models
from django.urls import reverse


class Country(models.Model):
    country = models.CharField(default="unknown", max_length=60)
    alpha2 = models.CharField(default="", max_length=2, unique=True)
    alpha3 = models.CharField(default="", max_length=3, unique=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['country']


class Rider(models.Model):
    name= models.CharField(max_length=100)
    birthday= models.DateField(null=True, blank=True)
    cqriderid= models.IntegerField(unique=True)
    uciid=models.IntegerField(null=True, blank=True)
    nationality=models.ForeignKey(Country, to_field='alpha3', db_constraint=False, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('rider-detail', args=[str(self.id)])


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
#    editie = models.ForeignKey(Edition, to_field='year', default="2019")
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


class Race(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    category = models.ForeignKey(Category, to_field='category', on_delete=models.SET_NULL, null=True)
    cqraceid = models.IntegerField(default=0, unique=True)
    country = models.ForeignKey(Country, to_field='alpha3', on_delete=models.SET_NULL, null=True, blank=True)

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


class Ploegleider(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    nickname = models.CharField(max_length=30, unique=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['-last_name']

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('ploegleider-detail', args=[str(self.id)])


class Edition(models.Model):
    year = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.year

    class Meta:
        ordering = ['-year']


class Verkocht(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ploegleider = models.ForeignKey(Ploegleider, on_delete=models.CASCADE)
    editie = models.ForeignKey(Edition, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    punten = models.FloatField(default=0)
    jpp = models.IntegerField(default=0)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('verkochterenners-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Verkochte renners'
