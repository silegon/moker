#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-05-15 09:54:36

from models import MokerResponse
from utils import copy_request

class MokerMiddleware(object):
    def process_response(self, request, response):
        if request.path.startswith('/send/'):
            copy_request(request)

            mo = MokerResponse()
            mo.url = request.get_full_path()
            response_headers = "".join(["%s:%s\n" % (key, value) for key, value in response._headers.values()])
            mo.body = response_headers + '\n\n' + response.content
            mo.save()
        return response
