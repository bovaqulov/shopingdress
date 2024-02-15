from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="kategorya")
    parent = models.ForeignKey("self", )