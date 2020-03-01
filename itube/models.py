from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def natural_key(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def natural_key(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Area(models.Model):
    id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=20)

    def __str__(self):
        return self.area_name


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    year = models.IntegerField(null=True)
    area = models.ForeignKey('itube.Area', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey('itube.Category', on_delete=models.CASCADE, primary_key=False)
    tags = models.ManyToManyField('itube.Tag', blank=True, null=True)
    videopic = models.ImageField(upload_to='videopic', blank=True, null=True)
    videocontent = models.FileField(upload_to='video', blank=True, null=True)

    def __str__(self):
        return self.title

# Create your models here.
