#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 19:14:23
import urllib2
import threading
import base64

from models import MokerRequest, MokerResponse, SEPERATOR

TIME_OUT = 5

def async_send_request(req, moker_response_id=False):
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
        response = urllib2.urlopen(self.req, None, TIME_OUT)
        if self.moker_response_id:
            moker_response = MokerResponse.objects.get(pk=self.moker_response_id)
            moker_response.body = SEPERATOR.join([str(response.headers), response.read()])
            moker_response.save()

def copy_request(request):
    mu = MokerRequest()
    mu.uri = request.build_absolute_uri()
    first_line = request.method + ' ' + request.build_absolute_uri() + ' ' + request.META['SERVER_PROTOCOL'] + '\n'
    request_headers = "".join(["%s:%s\n" % (header[5:], value) for header, value in request.META.items() if header.startswith('HTTP_')])
    mu.body = SEPERATOR.join([first_line, request_headers, request.body])
    mu.save()
def get_response(moker_request_id):
    send_request(moker_request_id, record_response=True)

def send_request(moker_request_id, record_response=False):
    moker_request = MokerRequest.objects.get(pk=moker_request_id)
    if moker_request.body:
        first_line, request_headers, request_body = moker_request.body.split(SEPERATOR)
        request_method, request_uri, request_protocal = first_line.split()
        request_headers_dict = {}
        for item in request_headers.split('\n'):
            if item:
                key, value = item.split(':', 1)
                request_headers_dict[key] = value.strip()
    else:
        request_body = None
        request_headers_dict = {}

    req = urllib2.Request(moker_request.uri, request_body, request_headers_dict)
    if record_response:
        moker_response = MokerResponse()
        moker_response.name = moker_request.name
        moker_response.moker_request = moker_request
        moker_response.save()
        async_send_request(req, moker_response.pk)
    else:
        async_send_request(req)

def moker_remote_data(request):
    content = eval(base64.b64decode(request.POST['data']))
    request_content = content['request_content']
    uri = request_content['uri']
    server_protocol = request_content['server_protocol']
    method = request_content['method']
    request_headers = request_content['request_headers']
    body = request_content['body']

    first_line = method + ' ' + uri + ' ' + server_protocol + '\n'
    request_body = SEPERATOR.join([first_line, request_headers, body])
    moker_request, created = MokerRequest.objects.get_or_create(uri=uri, body=request_body)

    if 'request_content' in content:
        response_content = content['response_content']
        response_headers = "".join(["%s: %s\n" % (key, value) for key, value in response_content['headers']])
        body = response_content['body']
        moker_response = MokerResponse()
        response_body = SEPERATOR.join([response_headers, body])
        moker_response, created = MokerResponse.objects.get_or_create(moker_request=moker_request, body=response_body)
