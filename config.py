#coding=utf-8
from libs.permission.permission_auth.permission_interface_libs import menu_permission
from libs.flash.flash_lib import get_flashed_messages

range_page = 5
settings = dict(
    template_path = 'templates',
    static_path = 'static',
    debug = True,
    cookie_secret = 'naskjaknda',
    login_url = '/auth/user_login',
    xsrf_cookies = True,
    ui_methods = {
        'menu_permission':menu_permission,
        'get_flashed_messages':get_flashed_messages,
    },
    # pycket的配置信息
    pycket = {
        'engine':'redis',
        'storage':{
            'host':'localhost',# 注意这个redis实在虚拟机上跑所以直接localhost
            'port':6379,
            'db_sessions':5,
            'db_notifications':11,
            'max_connections':2**31,
        },
        'cookies':{
            'expires_days':None,
            # 'max_age':100,
        }
    }

)