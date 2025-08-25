from django.conf import settings
from django.db import models


class ItemList(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
