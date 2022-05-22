from django.contrib import admin

# Register your models here.
from .models import Hotel,WishList

admin.site.register(Hotel)
admin.site.register(WishList)