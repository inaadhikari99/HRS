from django.contrib import admin

# Register your models here.
from .models import Hotel,WishList,Review

admin.site.register(Hotel)
admin.site.register(WishList)
admin.site.register(Review)