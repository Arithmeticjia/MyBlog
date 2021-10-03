from django import forms
from blog.models import Comment, Message, Articles

'''class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']'''


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ['name','email','text']
        exclude = ['name', 'email', 'post', 'parentcomment']


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256)


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # sex = forms.ChoiceField(label='性别', choices=gender)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['username', 'email', 'phone', 'title', 'content']


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        # fields = ('title', 'body')
        exclude = ['authorname', 'timestamp', 'tags', 'category', 'greats', 'comments', 'pic', 'brief', 'views',
                   'status', 'last_edit_timestamp', 'url_slug', 'rand_id']
