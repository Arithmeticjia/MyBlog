# Generated by Django 2.1.7 on 2020-03-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itube', '0003_video_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='unlike',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
