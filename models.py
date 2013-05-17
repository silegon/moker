#!/usr/bin/env python
# coding: utf-8

from django.db import models

SEPERATOR = "$$$$$$^^^$$$$$$$\n"

class MokerRequest(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    uri = models.URLField()
    body = models.TextField(verbose_name="原始请求", blank=True)

    class Meta:
        verbose_name = "mock请求"
        verbose_name_plural = "mock请求"

    def __unicode__(self):
        return "%s_%s_%s" % (self.name, self.id, self.uri)


class MokerResponse(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    moker_request = models.ForeignKey(MokerRequest, blank=True, verbose_name="对应请求")
    body = models.TextField(verbose_name="原始回复", blank=True)

    class Meta:
        verbose_name = "mock响应"
        verbose_name_plural = "mock响应"

    def __unicode__(self):
        return "%s_%s" % (self.name, self.id)
