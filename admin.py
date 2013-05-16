#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<code@forpm.net> 2013-03-25 14:02:39

from django.contrib import admin
from moker.models import MokerRequest, MokerResponse
from utils import get_response


class MokerRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','uri')
    list_editable = ('name',)
    actions = ['make_response']

    def make_response(self, request, queryset):
        for item in queryset:
            get_response(item.id)
    make_response.short_description = "生成HTTP Response"

class MokerResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','moker_request')
    list_editable = ('name',)

admin.site.register(MokerRequest, MokerRequestAdmin)
admin.site.register(MokerResponse, MokerResponseAdmin)
