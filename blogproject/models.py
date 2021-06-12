import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from uuslug import slugify
from blogproject.utils import generate_rich_content


class User(AbstractUser):
    mobile = models.CharField(max_length=16, null=True, default=None)
    profile_photo = models.ImageField(upload_to='userpic', blank=True, null=True)
    brief_info = models.CharField(max_length=200, blank=True, null=True)


class Category(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), editable=False, max_length=200, unique=True)

    def natural_key(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def natural_key(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = Choices(
        (1, "published", _("published")),
        (2, "draft", _("draft")),
        (3, "hidden", _("hidden")),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    excerpt = models.TextField(_("excerpt"), blank=True)
    views = models.PositiveIntegerField(_("views"), default=0, editable=False)
    created_time = models.DateTimeField(_("created time"), default=timezone.now)
    updated_time = models.DateTimeField(_("created time"), auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    url_slug = models.SlugField(editable=False, max_length=200)
    cover_pic = models.ImageField(upload_to='blogcovers')
    rand_id = models.CharField(max_length=8, default="1a2b3c4d")

    status = models.PositiveSmallIntegerField(
        _("status"), choices=STATUS_CHOICES, default=STATUS_CHOICES.draft
    )

    tags = models.ManyToManyField(Tag, verbose_name=_("tags"), blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Posts")
        verbose_name_plural = _("Posts")
        # ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:article_detail', args=[self.id])

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        if not self.excerpt:
            self.excerpt = strip_tags(self.content)[:150]

        if not self.created_time and self.status == self.STATUS_CHOICES.published:
            self.created_time = self.created_time

        if self.rand_id == "" or self.rand_id == "1a2b3c4d":
            self.rand_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def increase_views(self):
        self.__class__.objects.filter(id=self.id).update(views=F("views") + 1)

    def was_created_recently(self):
        # 若文章是"最近"发表的，则返回 True
        diff = timezone.now() - self.created_time
        if 0 == diff.days <= diff.seconds < 60:
            return True
        else:
            return False

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.content)

    @property
    def type(self):
        return "p"
