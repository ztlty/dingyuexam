# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import base64
import datetime
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from blueking.component.shortcuts import  get_client_by_user
from common.mymako import render_json
from home_application.models import OptLog


@task()
def async_task(bk_biz_id):
    """
    定义一个 celery 异步任务
    """
    # 创建操作记录
    client = get_client_by_user('dingyu')
    client.set_bk_api_ver('v2')
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "bk_job_id": 1019
    }
    res = client.job.execute_job(kwargs)
    task_id = res.get('data').get('job_instance_id')
    while not client.job.get_job_instance_status({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id,
    }).get('data').get('is_finished'):
        print 'waiting job finished...'
        time.sleep(1.2)

    res = client.job.get_job_instance_log({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id
    })

    log_content = res['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
    check_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    OptLog.objects.create(
        operator='dingyu',
        bk_biz_id=bk_biz_id,
        bk_job_id=task_id,
        opt_at=check_time,
        host_list=res['data'][0]['step_results'][0]['ip_logs'][0]['ip'],
        job_status=res['data'][0]['status'],
        job_content=log_content
    )


def execute_task(bk_biz_id):
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    async_task.delay(bk_biz_id)


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    pass
