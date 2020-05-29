from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Search(models.Model):
    searched_item = models.CharField(max_length=100)
    amazon_url = models.TextField(default='')
    ldlc_url = models.TextField(default='')
    maxgaming_url = models.TextField(default='')
    amazon_price = models.CharField(max_length=100, default='')
    ldlc_price = models.CharField(max_length=100, default='')
    maxgaming_price = models.CharField(max_length=100, default='')
    date_searched = models.DateTimeField(default=timezone.now)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.searched_item
