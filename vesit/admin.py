from django.contrib import admin

# Register your models here.
#from .models import *
from . import models

myModels = [models.Institute, models.Council, models.Council_Student, models.Committee, models.Team, models.Team_Student ]  # iterable list
admin.site.register(myModels)

