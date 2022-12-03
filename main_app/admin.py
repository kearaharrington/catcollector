from django.contrib import admin

from .models import Cat, Dog # use . because admin.py and models.py are in the same folder

# Register your models here.
admin.site.register(Cat)
admin.site.register(Dog)