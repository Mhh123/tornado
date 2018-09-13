# -*- coding:utf-8 -*-

# 拒绝隐式导入
from __future__ import absolute_import

from celery import Celery

celery_test = Celery('celery_tornado', include=['celery_test_module.celery_tasks'])

celery_test.config_from_object('celery_test_module.celery_config')

if __name__ == "__main__":
    celery_test.start()