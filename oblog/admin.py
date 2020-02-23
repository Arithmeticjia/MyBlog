from django.contrib import admin
from oblog.models import Articles,Tag
from . import models
#from guardian.admin import GuardedModelAdmin


# Register your models here.
class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'timestamp','authorname']

class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Articles, BlogsPostAdmin)
admin.site.register(Tag, BlogTagAdmin)
#admin.site.register(models.User)
admin.site.register(models.Message)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.BlogUser)
admin.site.register(models.Note)
admin.site.register(models.Picture)
# Register your models here.
