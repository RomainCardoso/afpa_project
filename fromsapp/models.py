from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Search(models.Model):
    searched_item = models.CharField(max_length=100)
    item_url = models.TextField()
    date_searched = models.DateTimeField(default=timezone.now)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.searched_item
