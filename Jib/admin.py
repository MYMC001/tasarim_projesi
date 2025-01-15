from django.contrib import admin
from django.contrib.auth.models import Permission ,User
from django.contrib.contenttypes.models import ContentType
from Jib.models import Restaurant

from .models import CustomUser

# Register your models here.
admin.site.register(Permission)
admin.site.register(CustomUser)
admin.site.register(ContentType)
admin.site.register(Restaurant)