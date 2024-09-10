from django.db import models
#for authentication
from django.contrib.auth.models import User
class recipe(models.Model):
    #authentication
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    Recipe_name=models.CharField(max_length=50)
    Recipe_description=models.TextField()
    Recipe_image=models.ImageField(upload_to="img")
