#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 19:14:23
import urllib2
import threading

from models import MokerRequest, MokerResponse

TIME_OUT = 5
SEPERATOR = "$$$$$$^^^$$$$$$$\n"

def async_send_request(req, moker_response_id):
    AsyncSendRequest(req, moker_response_id).start()

class AsyncSendRequest(threading.Thread):
    """
    send http request in thread, avoid time sleep relect to frontend.
    """
    def __init__(self, req, moker_response_id):
        threading.Thread.__init__(self)
        self.req = req
        self.moker_response_id = moker_response_id

    def run(self):
        self._async_send_request()

    def _async_send_request(self):
        try:
            response = urllib2.urlopen(self.req, None, TIME_OUT)
        except urllib2.URLError:
            response = None
        moker_response = MokerResponse.objects.get(pk=self.moker_response_id)
        if response:
            moker_response.body = SEPERATOR.join([str(response.headers), response.read()])
        else:
            moker_response.body = 'ERROR'
        moker_response.save()

def copy_request(request):
    mu = MokerRequest()
    mu.uri = request.build_absolute_uri()
    first_line = request.method + ' ' + request.build_absolute_uri() + ' ' + request.META['SERVER_PROTOCOL'] + '\n'
    request_headers = "".join(["%s:%s\n" % (header[5:], value) for header, value in request.META.items() if header.startswith('HTTP_')])
    mu.body = SEPERATOR.join(first_line, request_headers, request.body)
    mu.save()

def get_response(moker_request_id):
    moker_request = MokerRequest.objects.get(pk=moker_request_id)
    if moker_request.body:
        first_line, request_headers, request_body = moker_request.body.split("$$$$$")
        request_method, request_uri, request_protocal = first_line.split()
        request_headers_dict = {}
        for item in request_headers.split('\n'):
            key, value = item.split(':')
            request_headers_dict[key] = value.strip()
    else:
        request_body = None
        request_headers_dict = {} 

    moker_response = MokerResponse()
    moker_response.name = moker_request.name
    moker_response.moker_request = moker_request
    moker_response.save()

    req = urllib2.Request(moker_request.uri, request_body, request_headers_dict)
    async_send_request(req, moker_response.pk)
