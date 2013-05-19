#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 09:54:36

import urllib2
# use urllib2 for guest enviroment
import threading
import base64
from django.conf import settings
from django.core.handlers.wsgi import STATUS_CODE_TEXT

TIME_OUT = 3

def async_send_request(content):
    AsyncSendRequest(content).start()

class AsyncSendRequest(threading.Thread):
    """
    send http request in thread, avoid time sleep relect to frontend.
    """
    def __init__(self, content):
        threading.Thread.__init__(self)
        self.content = content

    def run(self):
        self._async_send_request()

    def _async_send_request(self):
        urllib2.urlopen(settings.MOKER_REQUEST_URL, "data=" + self.content, TIME_OUT)

def log_req(req):
    """
    记录某些需要发出的数据
    """
    request_content = {
        "uri" : req.get_full_url(),
        "server_protocol" : "HTTP/1.1",
        "method" : req.get_method(),
        "request_headers" : "".join(["%s: %s\n" % (key, value) for key, value in req.headers.items()]),
        "body" : req.data
    }
    content = {
        "request_content":request_content
    }
    async_send_request(base64.urlsafe_b64encode(str(content)))

class MokerMiddleware(object):
    def process_response(self, request, response):
        if request.path[-3:] not in ["jpg", "png", "css", ".js", "ion"]:
            request_content = {
                "uri" : request.build_absolute_uri(),
                "server_protocol" : request.META["SERVER_PROTOCOL"],
                "method" : request.method,
                "request_headers" : "".join(["%s: %s\n" % (header[5:], value) for header, value in request.META.items() if header.startswith("HTTP_")]),
                "body" : request.body,
            }
            response_content = {
                "server_protocol" : "HTTP/1.1",
                "msg" : STATUS_CODE_TEXT[response.status_code],
                "status_code" : response.status_code,
                "headers" : response.items(),
                "body" : response.content
            }
            content = {
                "request_content":request_content,
                "response_content":response_content
            }
            b64_content = base64.urlsafe_b64encode(str(content))
            async_send_request(b64_content)
        return response
