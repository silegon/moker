#!/usr/bin/env python
# coding: utf-8

from django.db import models
from django.conf import settings

ERROR_STATUS = "<ERROR>"

def request_status_line(method, uri, server_protocol):
    return "".join([method, " ", uri, " ",server_protocol])

def response_status_line(server_protocol, code, msg):
    return "".join([server_protocol, " ", code, " ", msg])

class MokerRequestManager(models.Manager):
    def o_create(self, method, uri, server_protocol, headers, body, check=False):
        status = request_status_line(method, uri, server_protocol)
        try:
            if settings.MOKER_CHECK_REQUEST_HEADERS:
                moker_request = MokerRequest.objects.get(status=status, headers=headers, body=body)
            else:
                moker_request = MokerRequest.objects.get(status=status, body=body)
            return moker_request, False
        except:
            moker_request = MokerRequest(status=status, headers=headers, body=body)
            if check:
                moker_request.name = ERROR_STATUS
            moker_request.save()
            return moker_request, True

class MokerRequest(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    status = models.CharField(max_length=255, verbose_name="请求状态")
    headers = models.TextField(blank=True, verbose_name="请求headers")
    body = models.TextField(blank=True, verbose_name="请求正文")
    objects = MokerRequestManager()

    class Meta:
        verbose_name = "mock请求"
        verbose_name_plural = "mock请求"

    def __unicode__(self):
        return "%s_%s_%s" % (self.name, self.id, self.uri)

class MokerResponseManager(models.Manager):
    def o_create(self, server_protocol, code, msg, headers, body, request=None, check=False):
        status = response_status_line(server_protocol, code, msg)
        try:
            if settings.MOKER_CHECK_REQUEST_HEADERS:
                moker_response = MokerResponse.objects.get(status=status, headers=headers, body=body, moker_request=request)
            else:
                moker_response = MokerResponse.objects.get(status=status, body=body, moker_request=request)
            return moker_response, False
        except:
            moker_response = MokerResponse(status=status, headers=headers, body=body, moker_request=request)
            if check:
                moker_response.name = ERROR_STATUS
            moker_response.save()
            return moker_response, True

class MokerResponse(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    moker_request = models.ForeignKey(MokerRequest, blank=True, verbose_name="对应请求")
    status = models.CharField(max_length=255, verbose_name="响应状态")
    headers = models.TextField(blank=True, verbose_name="响应headers")
    body = models.TextField(blank=True, verbose_name="响应正文")
    objects = MokerResponseManager()

    class Meta:
        verbose_name = "mock响应"
        verbose_name_plural = "mock响应"

    def __unicode__(self):
        return "%s_%s" % (self.name, self.id)
