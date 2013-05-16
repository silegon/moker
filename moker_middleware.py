#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 09:54:36

import urllib2
import threading
import base64

MOKER_REQUEST_URL = 'http://192.168.7.214:25001/' + 'mock_remote_request'
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
        urllib2.urlopen(MOKER_REQUEST_URL, 'data=' + self.content, TIME_OUT)

class MokerMiddleware(object):
    def process_response(self, request, response):
        if request.path.startswith('/tcms/j'):
            content = {
                'uri' : request.build_absolute_uri(),
                'server_protocol' : request.META['SERVER_PROTOCOL'],
                'method' : request.method,
                'request_headers' : "".join(["%s:%s\n" % (header[5:], value) for header, value in request.META.items() if header.startswith('HTTP_')]),
                'body' : request.body,
            }
            async_send_request(base64.b64encode(str(content)))
        return response
