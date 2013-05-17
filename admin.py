#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-03-25 14:02:39

from django.contrib import admin
from moker.models import MokerRequest, MokerResponse, SEPERATOR
from utils import send_request

def response_body_data(obj):
    if obj.body:
        headers, data = obj.body.split(SEPERATOR)
        if 'json' in headers:
            return data
        else:
            return data[:300]

def request_body_data(obj):
    if obj.body:
        return obj.body.split(SEPERATOR)[2]

class MokerRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','uri', request_body_data)
    list_editable = ('name',)
    actions = ['make_response']

    def make_response(self, request, queryset):
        for item in queryset:
            send_request(item.id)
    make_response.short_description = "生成HTTP Response"

class MokerResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','moker_request', response_body_data)
    list_editable = ('name',)

admin.site.register(MokerRequest, MokerRequestAdmin)
admin.site.register(MokerResponse, MokerResponseAdmin)
