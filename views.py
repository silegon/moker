#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-04-07 10:14:46

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from models import MokerRequest

from utils import moker_remote_data, send_request, mock_request

@csrf_exempt
def save_to_mock_request(request):
    # TODO
    mock_request(request)
    return HttpResponse('')

@csrf_exempt
def ajax(request):
    _p = request.POST
    type = _p.get("type", None)
    moker_request_id = _p.get("moker_request_id", None)
    if not type:
        return Http404
    AJAX_FUNC_DICT = {
        'send_moker_request':'send_request(moker_request_id)',
    }
    if type in AJAX_FUNC_DICT:
        response = eval(AJAX_FUNC_DICT[type])
        return HttpResponse(response)
    return Http404

def send(request, template_name='moker/send.html'):
    _g = request.GET
    request_id = _g.get('moker_request_id', '')
    if request_id:
        moker_request = get_object_or_404(MokerRequest, pk=request_id)
    else:
        moker_request = None

    moker_request_list = MokerRequest.objects.exclude(name='')
    context = {
        'moker_request_list' : moker_request_list,
        'moker_request' : moker_request
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))

@csrf_exempt
def moker_remote(request):
    moker_remote_data(request)
    return HttpResponse('')
