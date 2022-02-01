from django.contrib import admin
from . import models
from .models import Post, Category, Tag, User
from mdeditor.widgets import MDEditorWidget

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.MDTextField: {'widget': MDEditorWidget}
    }
    readonly_fields = ["views", "updated_time"]
    list_display = [
        "title",
        "id",
        "rand_id",
        "author",
        "status",
        "category",
        "views",
        "status",
        "url_slug",
    ]
    list_filter = [
        "status",
        "category",
        "tags",
        "created_time",
    ]
    # 搜索字段
    search_fields = ["title", "content"]
    # 详细时间分层筛选
    date_hierarchy = 'created_time'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    list_filter = [
        "name",
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]
    list_filter = [
        "name",
    ]


admin.site.register(models.User)
