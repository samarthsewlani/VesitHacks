from django.contrib import admin

# Register your models here.
from . import models

myModels = [models.Department, models.Staff, models.Student, ]  # iterable list
admin.site.register(myModels)
