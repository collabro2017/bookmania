from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from publisher.models import Book, BookPage, BookImage, BookComment
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from captcha.image import ImageCaptcha
import string
import random
from polli import constants
from django.db.models import Count, Q
import urllib2
import json
import time


def user_profile(request):
    context = {}
    return render(request, 'user/profile.html', context)


@csrf_exempt
def change_profile_pic(request):
    img_data = ContentFile(request.FILES['image'].read())

    user = request.user
    user.profile_pic.save('img_{}.jpg'.format(user.id), img_data)
    user.profile_pic_thumbnail.save('img_{}_thumbnail.jpg'.format(user.id), img_data)

    resp = {
        'url': user.profile_pic.url,
        'thumbnail_url': user.profile_pic_thumbnail.url,
        'msg': 'user profile pic updated'
    }

    return HttpResponse(json.dumps(resp))


@csrf_exempt
def update_profile(request):
    user = request.user
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.phone = request.POST['phone']
    user.save()

    resp = {
        'msg': 'user profile updated'
    }

    return HttpResponse(json.dumps(resp))
