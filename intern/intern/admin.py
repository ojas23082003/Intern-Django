from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Appointment)