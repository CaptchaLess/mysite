#!-*-utf8-*-
from django.http import HttpResponse
import requests
import tests
from CL_algorithm import *
import mis_test5
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


def processor(_url):
    _url = _url.replace(' ', '+')
    #assert False
    f = open('test', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    #assert False
    img_test = Image.open('test')
    yjs_epc = YJS_EPC()
    _result = yjs_epc.makePrediction_yjs(img_test)
    return _result

def processor_mis(_url):
    mis_alogrithm = MIS()
    _url = _url.replace(' ', '+')
    #assert False
    f = open('mis', 'wb')
    f.write(_url.decode('base64'))
    f.close()
    #assert False
    img_test = Image.open('mis')
    code_list = mis_test5.split_codes(img_test)
    list_len= len(code_list[0])
    list_type = type(code_list[0])
    #assert False
    _result = mis_alogrithm.makePrediction_mis_test(code_list)
    return _result 
	
	
