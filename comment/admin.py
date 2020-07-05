from django.contrib import admin

# Register your models here.
from comment import models

admin.site.register(models.Comment)