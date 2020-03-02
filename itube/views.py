from django.shortcuts import render,get_list_or_404,get_object_or_404
from itube.models import Tag, Category, Area, Video


def index(request):
    if request.method == "GET":
        channels = Video.objects.filter()[0:4]
        context = {
            "channels": channels
        }
        return render(request, 'itube/home.html', context=context)


def single_video(request, video_id):
    return render(request, 'itube/singlevideo.html')


def single_video_new(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    context = {
        "video": video
    }
    return render(request, 'itube/single-video.html', context=context)
# Create your views here.
