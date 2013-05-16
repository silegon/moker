#!/usr/bin/env python
# coding: utf-8

from django.db import models

class MokerRequest(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="类型名称")
    uri = models.URLField()
    body = models.TextField(verbose_name="原始请求", blank=True)

    class Meta:
        verbose_name = "Mock请求"
        verbose_name_plural = "Mock请求"

    def __unicode__(self):
        return "MokerRequest-%s-%s" % (self.id, self.name)


class MokerResponse(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    moker_request = models.ForeignKey(MokerRequest, blank=True, verbose_name="对应请求")
    body = models.TextField(verbose_name="原始回复", blank=True)

    class Meta:
        verbose_name = "Mock应答"
        verbose_name_plural = "Mock应答"

    def __unicode__(self):
        return "MokerResponse-%s-%s" % (self.id, self.name)
