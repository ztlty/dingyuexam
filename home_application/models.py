# -*- coding: utf-8 -*-
from django.db import models


class OptLog(models.Model):
    """操作记录信息"""
    operator = models.CharField(u'操作用户', max_length=128)
    bk_biz_id = models.CharField(u'业务', max_length=16)
    bk_job_id = models.CharField(u'作业ID', max_length=16)
    opt_at = models.CharField(u'操作时间', max_length=100)
    host_list = models.CharField(u'主机列表', max_length=100)
    job_status = models.CharField(u'作业状态', max_length=16)
    job_content = models.CharField(u'作业日志', max_length=1000)