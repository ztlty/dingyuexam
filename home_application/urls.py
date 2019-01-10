# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^api/test/$', 'test'),
    (r'^api/get_set/$', 'get_sets'),
    (r'^api/get_host/$', 'get_host'),
    (r'^api/fast_execute_script/$', 'fast_execute_script'),
    (r'^history/$', 'history')
)
