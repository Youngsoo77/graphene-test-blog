# -*- coding:utf-8 -*-
from django.db import models
from django.conf import settings
from base.models import BaseModel


class Post(BaseModel):
    title = models.CharField(help_text='제목', max_length=100, null=True, blank=True)
    content = models.TextField(help_text='내용', null=True, blank=True)
    published = models.NullBooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
