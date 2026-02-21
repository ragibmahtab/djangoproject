from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class event(models.Model):
#     name=models.CharField(max_length=200)
#     description=models.TextField()
#     date=models.DateField()
#     time=models.TimeField()
#     location=models.CharField(max_length=100)
#     catagory=models.ForeignKey("catagory", on_delete=models.CASCADE,default=1,related_name="catagorys")
#     #participant_set
#     #catagory_set
#     def __str__(self):
#         return self.name

class event(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=100)
    catagory=models.ForeignKey("catagory", on_delete=models.CASCADE,related_name="catagorys")

    image=models.ImageField(upload_to='event_images/', default='default.jpg')

    rsvp_users=models.ManyToManyField(User, related_name="rsvp_events", blank=True)

    def __str__(self):
        return self.name


    



# class participant(models.Model):
#     name=models.CharField(max_length=200)
#     email=models.EmailField(unique=True)
#     participated_event=models.ManyToManyField(event,related_name="participents")
    


class catagory(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.name
