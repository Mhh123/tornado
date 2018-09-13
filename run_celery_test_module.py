# -*- coding:utf-8 -*-
from celery_test_module.celery_tasks import add, manager_redis


# add.delay(5, 7)
# manager_redis.delay()

import time
for i in xrange(50):
    add.delay(i+1, 0)
    time.sleep(1)

# celery -A celery_test_module worker -l info -c 5  命令窗口执行的命令
# celery -A celery_test_module worker -l info -c 5 -B  加定时任务BEAT的启动的命令加上-B