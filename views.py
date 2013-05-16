#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-04-07 10:14:46

from django.shortcuts import render_to_response
from django.template import RequestContext

def send(request, template_name='moker/send.html'):
    context = {}
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
