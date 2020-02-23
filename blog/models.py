from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
from uuslug import slugify
from django.conf import settings
from datetime import date

'''class UserInfo(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)'''


class Category(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def natural_key(self):
        return self.__str__()

    def catcount(self):
        return Articles.objects.filter(category__name__exact=self.name).filter(status='有效').count()

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
        标签 Tag 也比较简单，和 Category 一样。
        再次强调一定要继承 models.Model 类！
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.


class Articles(models.Model):
    id = models.AutoField(primary_key=True)         # id
    title = models.CharField(max_length=150)        # 博客标题
    # body = models.TextField()  # 博客正文
    body = MDTextField()
    timestamp = models.DateTimeField()  # 创建时间
    authorname = models.ForeignKey('blog.BlogUser', on_delete=models.CASCADE)  # 作者姓名
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, primary_key=False)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    greats = models.PositiveIntegerField(default=0)
    comments = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="DEL")
    brief = models.CharField(max_length=200, blank=True, null=True)
    pic = models.ImageField(upload_to='jiablogimages')
    # bodypic = models.ImageField(upload_to='jiablogimages', blank=True, null=True)
    istop = models.CharField(max_length=5, default='', null=True, blank=True)
    articlebodybrief = models.TextField(blank=True, null=True)
    last_edit_timestamp = models.DateTimeField(auto_now=True, verbose_name="更新时间", editable=True)
    url_slug = models.SlugField(editable=False, max_length=200)

    pic_800_450 = ImageSpecField(
        source="pic",
        processors=[ResizeToFill(800, 450)],
        format='JPEG',
        options={'quality': 95}
    )

    # 访问量

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        return self.views

    @property
    def all_comments(self):
        return self.comment_set.all()

    def article_greats(self):
        return self.greats

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.title)
        super(Articles, self).save(*args, **kwargs)


# Create your models here.


class Comment(models.Model):
    name = models.ForeignKey('blog.BlogUser', max_length=100, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    # email = name.email
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Articles', on_delete=models.CASCADE)
    parentcomment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text[:20]

    def ifnochild(self):
        '''if Comment.objects.filter(comment__comment__post_id=self.post_id).count() == 0:
            print('1')
            return True
            else:
            return False'''
        if self.comment_set.all().count() != 0:
            return 1
        else:
            return 0


class Message(models.Model):
    username = models.CharField(max_length=256)
    title = models.CharField(max_length=512)
    content = models.TextField(max_length=256)
    email = models.EmailField()
    publish = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=11, blank=True, default="", null=True)
    messpic = models.CharField(max_length=50, null=True)

    # 为了显示
    def __str__(self):
        tpl = '<Message:[username={username}, title={title}, content={content}, publish={publish}]>'
        return tpl.format(username=self.username, title=self.title, content=self.content, publish=self.publish)


class Note(models.Model):
    content = models.CharField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)
    noteimage = models.ImageField(upload_to='noteimg')


class Version(models.Model):
    version_time = models.DateField()
    version_content = models.CharField(max_length=1000)


class BlogRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ('add_user_per', '添加用户权限'),
            ('del_user_per', '删除用户权限'),
            ('change_user_per', '修改用户权限'),
            ('sel_user_per', '查询用户权限')
        )

    def __str__(self):
        return self.name


class BlogUserCollect(models.Model):
    id = models.AutoField(primary_key=True)
    blogid = models.CharField(max_length=15)
    userid = models.CharField(max_length=15)


class BlogUser(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    status = (
        ('active', '有效'),
        ('disabled', '无效'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    userpic = models.ImageField(upload_to='userpic', blank=True, null=True)
    status = models.CharField(max_length=32, choices=status, default='有效')
    brief = models.CharField(max_length=1024, blank=True, null=True)
    role = models.ManyToManyField(BlogRole, blank=True, null=True)

    def natural_key(self):
        return self.__str__()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# class BlogAuth(models.Model):
#     id = models.AutoField(primary_key=True)
#     class Meta:
#         permissions = (
#             ('add_user_per', '添加用户权限'),
#             ('del_user_per', '删除用户权限'),
#             ('change_user_per', '修改用户权限'),
#             ('sel_user_per', '查询用户权限')
#         )

class Sysrecord(models.Model):
    id = models.AutoField(primary_key=True)
    cpu = models.FloatField()
    mem = models.FloatField()
    disk_usage = models.FloatField()


# 访问网站的ip地址和次数
class Userip(models.Model):
    ip = models.CharField(verbose_name='IP地址', max_length=30)  # ip地址
    count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


# 网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.PositiveSmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class Recruitment(models.Model):
    is_not = (
        ('yes', '是'),
        ('no', '否'),
    )
    company_name = models.CharField(max_length=50)
    industry_name = models.CharField(max_length=50)
    is_form = models.CharField(max_length=10, choices=is_not)
    if_accept = models.CharField(max_length=50)
    des = models.CharField(max_length=50)


class Recruinfo(models.Model):
    company_name = models.CharField(max_length=30)
    job = models.CharField(max_length=50)
    info = models.TextField()


# create_time = models.DateTimeField()


class CodeModel(models.Model):
    name = models.CharField(max_length=50)  # 名字最长为 50 个字符
    code = models.TextField()  # 这个字段没有文本长度的限制

    def __str__(self):
        return 'Code(name={},id={})'.format(self.name, self.id)


class ArticleBodyPic(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.CharField(max_length=20, blank=True, null=True)
    pic = models.ImageField(upload_to='articlebodypics', blank=True, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.CharField(max_length=16, unique=True, primary_key=True)
    title = models.CharField(max_length=128)
    year = models.IntegerField(null=True)
    area = models.ForeignKey('blog.Area', on_delete=models.CASCADE, blank=True, null=True)
    # area = models.CharField(max_length=20,blank=True,null=True)
    genres = models.ManyToManyField(Genre, related_name='movies', db_table='movie_genre')
    filmpic = models.ImageField(upload_to='filmpics', blank=True, null=True)

    def __str__(self):
        return self.title


class Area(models.Model):
    id = models.AutoField(primary_key=True)
    area_id = models.CharField(max_length=10)
    area_name = models.CharField(max_length=20)

    def __str__(self):
        return self.area_name


class JiaFile(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=500)
    file_url = models.CharField(max_length=500)
    file_status = models.CharField(max_length=2)

    def __str__(self):
        return self.file_name


class params(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    param_value = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Jia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    brief = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='jia', blank=True, null=True)
# Create your models here.


class Graduation(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=150)


class Honour(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=150)


class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=300)


class Teacher(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    userpic = models.ImageField(upload_to='userpic', blank=True, null=True)
    brief = models.CharField(max_length=100)
    study_about = models.CharField(max_length=200)
    # graduation = models.ForeignKey('Graduation',on_delete=models.CASCADE)
    # Honour = models.ForeignKey('Honour',on_delete=models.CASCADE)
    personal_phone = models.CharField(max_length=15)
    office_phone = models.CharField(max_length=15)
    office_address = models.CharField(max_length=20)
    info = models.CharField(max_length=100)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(max_length=300)


class Hits(models.Model):
    userid = models.IntegerField(default=0)
    blogid = models.IntegerField(default=0)
    hitnum = models.IntegerField(default=0)

    def __str__(self):
        return BlogUser.objects.get(id=self.userid).name

    class Meta:
        verbose_name = "点击量"
        verbose_name_plural = "点击量"
