#!-*-utf8-*-
from django.http import HttpResponse
import requests
import tests
from CL_algorithm import *
import  mis_classify
import mis_test5
import Image
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
    result = processor_mis(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def weibo(request):
    image_url = request.GET['url']
    result = processor(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def lib(request):
    image_url = request.GET['url']
    result = processor_lib(image_url)

    response = HttpResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def processor(_url):
    _url = _url.replace(' ', '+')
    #assert False
    f = open('tmp.png', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    #assert False
    img_test = Image.open('tmp.png')
    #img_test_shape = img_test.shape
#    assert False
    yjs_epc = YJS_EPC()
    _result = yjs_epc.makePrediction_yjs(img_test)
    return _result

def processor_lib(_url):
    _url = _url.replace(' ', '+')
    f = open('tmp.png', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    img_test = Image.open('tmp.png')
    #img_test_shape = img_test.shape
    lib = LIB()
    result = lib.predict(img_test)
    return result

def processor_mis(_url):
    mis_alogrithm = MIS()
    _url = _url.replace(' ', '+')
    #assert False
    f = open('tmp.png', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    #assert False
    img_test = Image.open('tmp.png')
    _result = mis_classify.test(img_test, './checkcode/template_rgb/')
    return _result 
	
	
