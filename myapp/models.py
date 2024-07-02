from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    uid = models.CharField(max_length=24, unique=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    imageUrl = models.CharField(max_length=500, blank=True, null=True)
    webSales = models.CharField(max_length=255, blank=True, null=True)
    sourceWebPromote = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    editModifyDate = models.DateTimeField(blank=True, null=True)
    sourceWebName = models.CharField(max_length=255, blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    hitRate = models.IntegerField(blank=True, null=True)
    

class EventUnit(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    unitType = models.CharField(max_length=50)
    unitName = models.CharField(max_length=255)

class Location(models.Model):
    locationName = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

class ShowInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
