from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    salt = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'




