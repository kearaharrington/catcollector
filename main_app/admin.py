from django.contrib import admin

from .models import Cat # use . because admin.py and models.py are in the same folder

# Register your models here.
admin.site.register(Cat)