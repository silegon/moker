#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-03-25 14:02:39

from django.contrib import admin
from moker.models import MokerRequest, MokerResponse
from utils import send_request

def response_body_data(obj):
    return obj.body[:300]

def request_body_data(obj):
    return obj.body[:300]

class MokerRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','status', 'headers', request_body_data)
    list_editable = ('name',)
    actions = ['make_response']

    def make_response(self, request, queryset):
        for item in queryset:
            send_request(item.id)
    make_response.short_description = "生成HTTP Response"

class MokerResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','status', 'moker_request','headers', response_body_data)
    list_editable = ('name',)

admin.site.register(MokerRequest, MokerRequestAdmin)
admin.site.register(MokerResponse, MokerResponseAdmin)
