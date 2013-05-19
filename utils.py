#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 19:14:23
import requests
#TODO 好像只有send_request 需要改
import threading
import base64

from models import MokerRequest, MokerResponse

TIME_OUT = 5

def headers_string_to_dict(headers_string):
    headers_dict = {}
    for header_line in headers_string.splitlines():
        key, value = header_line.split(": ")
        headers_dict[key] = value
    return headers_dict

def headers_dict_to_string(headers_dict):
    return "".join(["%s: %s\n" % (key, value) for key, value in headers_dict.items()])

def django_request_headers_to_string(request):
    return "".join(["%s: %s\n" % (header[5:], value) for header, value in request.META.items() if header.startswith("HTTP_")])

def async_send_request(moker_request_id):
    AsyncSendRequest(moker_request_id).start()

class AsyncSendRequest(threading.Thread):
    """
    send http request in thread, avoid time sleep relect to frontend.
    """
    def __init__(self, moker_request_id):
        threading.Thread.__init__(self)
        self.moker_request_id = moker_request_id

    def run(self):
        self._async_send_request()

    def _async_send_request(self):
        moker_request = MokerRequest.objects.get(pk=self.moker_request_id)
        request_method, request_uri, server_protocol = moker_request.status.split(" ")
        request_headers = headers_string_to_dict(moker_request.headers)

        if request_method == "GET":
            response = requests.get(request_uri, headers=request_headers)
        elif request_method == "POST":
            response = requests.post(request_uri, headers=request_headers, data=moker_request.body)
        else:
            raise

        response_headers = headers_dict_to_string(response.headers)
        moker_response, created = MokerResponse.objects.o_create("HTTP/1.1", response.status_code, response.reason, response_headers, response.content, request=moker_request)

def mock_request(request):
    uri = request.build_absolute_uri()
    server_protocol = request.META["SERVER_PROTOCOL"]
    method = request.method
    request_headers = django_request_headers_to_string(request)
    body = request.body
    moker_request, created = MokerRequest.objects.o_create(method, uri, server_protocol, request_headers, body)

def send_request(moker_request_id):
    async_send_request(moker_request_id)

def moker_remote_data(request):
    b64_content = base64.urlsafe_b64decode(str(request.POST['data']))
    content = eval(b64_content)
    request_content = content['request_content']
    uri = request_content['uri']
    server_protocol = request_content['server_protocol']
    method = request_content['method']
    request_headers = request_content['request_headers']
    body = request_content['body']

    moker_request, created = MokerRequest.objects.o_create(method, uri, server_protocol, request_headers, body)

    if "response_content" in content:
        response_content = content['response_content']
        server_protocol = response_content['server_protocol']
        status_code = response_content['status_code']
        status_msg = response_content['msg']
        response_headers = "".join(["%s: %s\n" % (key, value) for key, value in response_content['headers']])
        moker_response, created = MokerResponse.objects.o_create(server_protocol, status_code ,status_msg , response_headers, response_content['body'], request=moker_request)
