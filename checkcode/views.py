#!-*-utf8-*-
from django.http import HttpResponse
import requests
import tests
from PIL import Image
# Create your views here
# process the checkcode function

from django.http import HttpResponseRedirect


def yjs_epc(request):
    image_url = request.GET['url']
    result = processor(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def mis(request):
    image_url = request.GET['url']
    result = processor(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def weibo(request):
    image_url = request.GET['url']
    result = processor(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def processor(_url):
    _url = _url.replace(' ', '+')
    #assert False
    f = open('test', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    #assert False
    img_test = Image.open('test')
    _result = tests.makePrediction_yjs(img_test)
    return _result
