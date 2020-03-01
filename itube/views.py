from django.shortcuts import render
from itube.models import Tag, Category, Area, Video


def index(request):
    return render(request, 'itube/home.html')


def single_video(request, video_id):
    return render(request, 'itube/singlevideo.html')


def single_video_new(request,video_id):
    return render(request, 'itube/single-video.html')
# Create your views here.
