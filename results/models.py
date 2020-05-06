from django.db import models


class Rider(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    CQranking_id = models.IntegerField()
    UCI_id = models.IntegerField()
#    nationality = models.ForeignKey

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=20)
    category_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'UCI-category'
        verbose_name_plural = 'UCI-Categories'


class RacePoints(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ranking = models.CharField(max_length=50)
    points = models.FloatField()

    class Meta:
        verbose_name = 'Punten per race'
        verbose_name_plural = 'Punten per race'


class Race(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rank = models.CharField(max_length=20)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ploegleider(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return self.name


class VirtualTeam(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ploegleider = models.ForeignKey(Ploegleider,  on_delete=models.CASCADE)
    editie = models.IntegerField()
    price = models.IntegerField()
