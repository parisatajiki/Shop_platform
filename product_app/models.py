from django.db import models
from autoslug import AutoSlugField

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title',unique=True,blank=True,null=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)

    def __str__(self):
        return self.title



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,related_name='product', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product', blank=True, null=True)
    price = models.IntegerField()
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True)


    def __str__(self):
        return self.title

