#coding=utf-8
import functools
from models.permission.permission_model import Handler,Menu
from libs.flash.flash_lib import flash
obj_model = {
    "handler": Handler,
    "menu": Menu,
}

class PermissionAuth(object):
    def __init__(self):
        self.user_permission = set()
        self.obj_permission = ''

    def permission_auth(self, user, name, types, model):
        #获取当前用户的权限
        roles = user.roles
        for role in roles:
            for permission in role.permissions:
                self.user_permission.add(permission.strcode)
        #获取要操作的handler处理的权限

        # obj_model = {
        #     "handler": Handler,
        #     "menu": Menu,
        # }
        # model = obj_model
        handler = model[types].by_name(name)

        if handler is None:
            return

        permission = handler.permission
        self.obj_permission = permission.strcode
        #判断用户有没有这个handler操作的权限
        if self.obj_permission in self.user_permission:
            return True
        return False

def handler_permission(handlername,types):
    """

    :param handlername:
    :param types:
    :return:
    example:
            @handler_permission('DelPermissionHandler', 'handler')
    """
    def func(method):
        @functools.wraps(method)
        def wrapper(self,*args,**kwargs):
            if PermissionAuth().permission_auth(self.current_user, handlername, types,obj_model):
                return method(self,*args,**kwargs)
            else:
                flash(self,'没有删除的权限','error')
                self.redirect('/permission/manage_list')
                # self.write('没有删除角色的权限')
        return wrapper
    return func


def menu_permission(self,menuname,types):
    if PermissionAuth().permission_auth(self.current_user, menuname, types, obj_model):
        return True
    return False
