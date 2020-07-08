import markdown
from django.shortcuts import render, get_object_or_404
from django.views import View
from markdown.extensions.toc import TocExtension, slugify
from blogproject.models import Post, Category
from comment.models import Comment


# Create your views here.

def post_detail_test(request, article_id, url_slug):
    pass


def post_detail(request, article_id, url_slug):

    try:
        post = get_object_or_404(Post, id=article_id)
        post.increase_views()
        if post.url_slug != url_slug:
            return render(request, '404.html')
    except Exception as e:
        return render(request, '404.html')
    likes = post.likes
    category_id = post.category.id
    tag_name = post.tags.values('name')
    category = get_object_or_404(Category, id=category_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)
    ])
    post.content = md.convert(post.content)
    comments = Comment.objects.filter(post=article_id)
    context = {
        'post': post,
        'category': category,
        'tag': tag_name,
        'likes': likes,
        'toc': md.toc,
        'comments': comments

    }
    return render(request, 'blogproject/single.html', context=context)


class PostDetailView(View):

    def get(self, request, article_id, url_slug):

        try:
            post = get_object_or_404(Post, id=article_id)
            if post.url_slug != url_slug:
                return render(request, '404.html')
        except Exception as e:
            return render(request, '404.html')
        likes = post.likes
        category_id = post.category.id
        tag_name = post.tags.values('name')
        category = get_object_or_404(Category, id=category_id)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        context = {
            'post': post,
            'category': category,
            'tag': tag_name,
            'likes': likes,
            'toc': md.toc,
        }
        return render(request, 'blogproject/single.html', context=context)