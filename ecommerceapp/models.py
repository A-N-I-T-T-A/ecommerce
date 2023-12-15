from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=255)
class product(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    pdname=models.CharField(max_length=255)
    pdprice=models.IntegerField()
    pd_desc=models.CharField(max_length=255)
    pdimage=models.ImageField(upload_to="image/",null=True)
class userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    prf_image=models.ImageField(upload_to="image/",null=True)
class cart1(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(product,on_delete=models.CASCADE,null=True)