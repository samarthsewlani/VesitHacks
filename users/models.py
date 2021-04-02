from django.db import models
from PIL import Image
#from vesit.models import Department
from django import forms

# Create your models here.
class Department(models.Model):
    name = models.CharField( max_length= 100 )

    def __str__(self):
        return "Department: "+self.name

class Student(models.Model):
    name = models.CharField( max_length=50 )
    email = models.EmailField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T','Transgender'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    iid = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=10)
    image = models.ImageField(default = "default.jpg", upload_to = 'student-profile')

    dept = models.ForeignKey( Department, on_delete = models.CASCADE )
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "Student: "+ str(self.name)

    def save(self,*args,**kwargs):              #Overriding save method to set size of the image
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img=img.resize(output_size)
            img.save(self.image.path)


class Staff(models.Model):
    name = models.CharField( max_length=50 )
    email = models.EmailField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T','Transgender'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    eid = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=10)
    image = models.ImageField(default = "default.jpg", upload_to = 'staff-profile')
    password = models.CharField(max_length=100, null=True)

    STAFF_CHOICES = (
        ('H', 'Head of Department'),
        ( 'P', 'Proffesor' ),
        ( 'A', 'Assistant Proffesor' ),
        ( 'L', 'Lab incharge'  ),
        ('Z', 'Principal')
    )
    staff_type = models.CharField(max_length=1, choices=STAFF_CHOICES)
    dept = models.ForeignKey( Department, on_delete = models.CASCADE )

    def __str__(self):
        return "Staff: "+ str(self.name)

    def save(self,*args,**kwargs):              #Overriding save method to set size of the image
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img=img.resize(output_size)
            img.save(self.image.path)
            


