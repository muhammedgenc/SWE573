from django.contrib import admin
from .models import Service, UserProfile, ServiceApplication,Event, EventApplication

admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(ServiceApplication)
admin.site.register(Event)
admin.site.register(EventApplication)