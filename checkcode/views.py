#!-*-utf8-*-
from django.http import HttpResponse
import requests
import tests
from PIL import Image
# Create your views here
# process the checkcode function

from django.http import HttpResponseRedirect


def yjs(request):
    image_url = request.GET['url']
    # image_url = "http://yjs.ustc.edu.cn/checkcode.asp"
    result = prcessor(image_url)
    # TODO
    return HttpResponse(result)


def mis(request):
    image_url = request.GET['url']
    result = prcessor(image_url)
    return HttpResponse(result)


def epc(request):
    image_url = request.GET['url']
    result = prcessor(image_url)
    return HttpResponse(result)


def weibo(request):
    image_url = request.GET['url']
    result = prcessor(image_url)
    return HttpResponse(result)


def prcessor(_url):
    r = requests.get(_url)
    with open('test', 'wb') as data:
        data.write(r.content)
        data.close()
    img_test = Image.open("test")
    _result = tests.makePrediction_yjs(img_test)
    return _result
