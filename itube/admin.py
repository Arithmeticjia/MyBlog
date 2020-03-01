from django.contrib import admin
from itube import models

admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Area)
admin.site.register(models.Video)

# Register your models here.
