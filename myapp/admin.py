from django.contrib import admin
from .models import Event, EventUnit, Location, ShowInfo

admin.site.register(Event)
admin.site.register(EventUnit)
admin.site.register(Location)
admin.site.register(ShowInfo)

