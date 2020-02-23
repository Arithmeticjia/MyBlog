from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser




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
    name = models.CharField(max_length=100)
    def catcount(self):
        return Articles.objects.filter(category__name__exact=self.name).filter(status='有效').count()


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100)

# Create your models here.


class Articles(models.Model):
    id = models.AutoField(primary_key=True)                         # id
    title = models.CharField(max_length = 150)                      # 博客标题
    body = models.TextField()                                       # 博客正文
    timestamp = models.DateTimeField()                              # 创建时间
    authorname = models.ForeignKey('oblog.BlogUser',related_name='authorname_id',on_delete=models.CASCADE)        # 作者姓名
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True,null=True)
    greats = models.PositiveIntegerField(default=0)
    comments = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="DEL")
    brife =  models.CharField(max_length=1000,blank=True)
    pic = models.ImageField(upload_to='blogimages')

    # 访问量

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        return self.views

    @ property
    def all_comments(self):
        return self.comment_set.all()

    def article_greats(self):
        return self.greats
# Create your models here.




class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    #url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('oblog.Articles',on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]


class Message(models.Model):
    username=models.CharField(max_length=256)
    title=models.CharField(max_length=512)
    content=models.TextField(max_length=256)
    email = models.EmailField()
    publish=models.DateTimeField(auto_now_add=True)
    phone=models.CharField(max_length=11,blank=True,default="",null=True)

    # 为了显示
    def __str__(self):
        tpl = '<Message:[username={username}, title={title}, content={content}, publish={publish}]>'
        return tpl.format(username=self.username, title=self.title, content=self.content, publish=self.publish)


class Note(models.Model):
    content =  models.CharField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)
    noteimage = models.ImageField(upload_to='noteimg')


class Picture(models.Model):
    pic = models.ImageField(upload_to='images')


class BlogUser(models.Model):
    '''用户表'''
    
    gender = (
              ('male','男'),
              ('female','女'),
              )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)
              
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
