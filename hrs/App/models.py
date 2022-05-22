from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=100,db_index=True,unique=True)
    price = models.BigIntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    cuisine = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = ' Wishlist '


