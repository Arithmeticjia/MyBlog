from django.contrib import admin
from . import models
from mdeditor.widgets import MDEditorWidget


class BlogsPostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.MDTextField: {'widget': MDEditorWidget}
    }
    search_fields = ('title', 'body')
    list_display = ['title', 'body', 'timestamp', 'authorname']


admin.site.register(models.Articles, BlogsPostAdmin)
admin.site.register(models.Message)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Note)
admin.site.register(models.Version)
admin.site.register(models.BlogUser)
admin.site.register(models.Sysrecord)
admin.site.register(models.Userip)
admin.site.register(models.VisitNumber)
admin.site.register(models.DayNumber)
admin.site.register(models.SocialAuthUsersocialauth)
admin.site.register(models.AuthUser)
admin.site.register(models.DjangoContentType)
admin.site.register(models.SocialAuthPartial)
admin.site.register(models.SocialAuthNonce)
admin.site.register(models.SocialAuthCode)
admin.site.register(models.SocialAuthAssociation)
admin.site.register(models.Recruitment)
admin.site.register(models.Recruinfo)
admin.site.register(models.CodeModel)
admin.site.register(models.ArticleBodyPic)
admin.site.register(models.Genre)
admin.site.register(models.Movie)
admin.site.register(models.Area)
admin.site.register(models.JiaFile)
admin.site.register(models.params)
admin.site.register(models.Jia)
admin.site.register(models.BlogUserCollect)
admin.site.register(models.Hits)
admin.site.register(models.LoveFZY)

# Register your models here.
