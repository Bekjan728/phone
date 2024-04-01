from django.contrib import admin

from .models import (
    Brand, 
    Phone,
    Model
)

admin.site.register([Brand, Phone, Model])
