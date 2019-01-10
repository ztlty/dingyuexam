# -*- coding: utf-8 -*-

from blueking.component.shortcuts import get_client_by_request
from common.log import logger
from common.mymako import render_mako_context, render_json,render_mako_tostring
from home_application import celery_tasks
import datetime

def home(request):
    """
    首页
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    # 查询业务
    res = client.cc.search_business()

    if res.get('result', False):
        bk_biz_list = res.get('data').get('info')
    else:
        logger.error(u"请求业务列表失败：%s" % res.get('message'))
        bk_biz_list = []
    return render_mako_context(request, '/home_application/home.html', {
        'bk_biz_list': bk_biz_list,
    })


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    data = {}
    data['user'] = "<"+request.user.username+">"
    data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_json({
        'result': 'true',
        'data': data,
        'message': 'success'})


def get_sets(request):
    bk_biz_id = int(request.GET.get('bk_biz_id'))
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    # 查询集群
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "bk_supplier_account": 0,
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_set_name"
        },
        "condition": {
        },
        "fields": [
            "bk_set_name",
            "bk_set_id"
        ]
    }
    res = client.cc.search_set(kwargs)
    data = render_mako_tostring('/home_application/tbody-set.html', {
        'bk_set_list': res.get('data').get('info')
    })
    return render_json({
        'result': True,
        'data': data
    })


def get_host(request):
    """
    获取主机
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    bk_biz_id = request.GET["bk_biz_id"]
    bk_set_id = request.GET["bk_set_id"]
    res = client.cc.search_host({
        "page": {"start": 0, "limit": 10, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [
                ],
                "condition": []
            },
            {"bk_obj_id": "module", "fields": [], "condition": []},
            {"bk_obj_id": "set", "fields": [], "condition": [
                {
                    "field": "bk_set_id",
                    "operator": "$eq",
                    "value": int(bk_set_id)
                }
            ]},
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": int(bk_biz_id)
                    }
                ]
            }
        ]
    })

    if res.get('result', False):
        bk_host_list = res.get('data').get('info')
    else:
        bk_host_list = []
        logger.error(u"请求主机列表失败：%s" % res.get('message'))

    bk_host_list = [
        {
            'bk_host_innerip': host['host']['bk_host_innerip'],
            'bk_host_name': host['host']['bk_host_name'],
            'bk_host_id': host['host']['bk_host_id'],
            'bk_os_type': host['host']['bk_os_type'],
            'bk_os_name': host['host']['bk_os_name'],
            'bk_cloud_id': host['host']['bk_cloud_id'][0]['bk_inst_id'],
            'bk_cloud_name': host['host']['bk_cloud_id'][0]['bk_inst_name'],
            'bk_set_name': ' '.join(map(lambda x: x['bk_set_name'], host['set'])[:1]),
            'bk_module_name': ' '.join(map(lambda x: x['bk_module_name'], host['module'])[:1]),
        }
        for host in bk_host_list
    ]
    data = render_mako_tostring('/home_application/tbody-ip.html', {
        'bk_host_list': bk_host_list
    })
    return render_json({
        'result': True,
        'data': data
    })


def fast_execute_script(request):
    """快速执行脚本"""
    bk_biz_id = int(request.POST.get('bk_biz_id'))
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "bk_job_id": 1019
    }
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    result = client.job.get_job_detail(kwargs)
    result = client.job.execute_job(kwargs)
    result = client.job.get_job_instance_log(kwargs)
    return render_json({
        'result': True,
        'data': '提交成功' })


def history(request):
    """
    操作历史
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')

    # 查询业务
    res = client.cc.search_business()
    bk_biz_list = res.get('data').get('info')

    return render_mako_context(request,
                               '/home_application/his.html', {
                                   'bk_biz_list': bk_biz_list,
                               })
