#coding=utf-8
from tornado.web import authenticated
from libs.permission.permission_auth.permission_interface_libs import handler_permission
from handlers.base.base_handler import BaseHandler
from libs.permission.permission_libs import (
                                                permission_manage_list_lib,
                                                add_role_lib,
                                                del_role_lib,
                                                add_permission_lib,
                                                del_permission_lib,
                                                add_menu_lib,
                                                del_menu_lib,
                                                add_handler_lib,
                                                del_handler_lib,
                                                add_user_role_lib,
                                                add_role_permission_lib,
                                                del_user_lib,
                                                add_user_dev_role_lib,
                                                del_user_role_lib,
                                                del_user_for_one_role_lib,
                                             )
class ManageHandler(BaseHandler):
    """01权限管理页面函数"""
    @authenticated
    def get(self):
        roles,permissions,menus,handlers,users,dev_users,dev_roleid= permission_manage_list_lib(self)
        kw = {
            'roles':roles,
            'permissions':permissions,
            'menus':menus,
            'handlers':handlers,
            'users':users,
            'dev_users':dev_users,
            'dev_roleid':dev_roleid
        }
        self.render('permission/permission_list.html', **kw)

class AddRoleHandler(BaseHandler):
    """02添加角色"""
    def post(self):
        name = self.get_argument('name','')
        add_role_lib(self,name)
        self.redirect('/permission/manage_list')


class DelRoleHandler(BaseHandler):
    """03删除角色"""
    # @handler_permission('DelRoleHandler','handler')
    def get(self):
        roleid = self.get_argument('id','')
        del_role_lib(self,roleid)
        print('123')
        self.redirect('/permission/manage_list')


class AddPermissionHandler(BaseHandler):
    """04添加权限"""
    def post(self):
        name = self.get_argument('name','')
        strcode = self.get_argument('strcode','')
        add_permission_lib(self,name,strcode)
        self.redirect('/permission/manage_list')


class DelPermissionHandler(BaseHandler):
    """05删除权限"""

    @handler_permission('DelPermissionHandler', 'handler')
    def get(self):
        permissionid = self.get_argument('id','')
        del_permission_lib(self,permissionid)
        self.redirect('/permission/manage_list')


class AddMenuHandler(BaseHandler):
    """06添加菜单并为菜单添加权限"""
    def post(self):
        name = self.get_argument('name','')
        permissionid = self.get_argument('permissionid','')
        add_menu_lib(self,name,permissionid)
        self.redirect('/permission/manage_list')


class DelMenuHandler(BaseHandler):
    """07为菜单删除权限"""
    # 其实这里只删除了menu，因为menu.permission这个对象是基于menu的
    # 所以只要删除了menu，那么基于它之上的都会被删除
    def get(self):
        menuid = self.get_argument('menuid','')
        del_menu_lib(self,menuid)
        self.redirect('/permission/manage_list')


class AddHandlerHandler(BaseHandler):
    """08为处理器添加权限"""
    def post(self):
        name = self.get_argument('name','')
        permissionid = self.get_argument('permissionid','')
        add_handler_lib(self,name,permissionid)
        self.redirect('/permission/manage_list')


class DelHandlerHandler(BaseHandler):
    """09删除处理器"""
    def get(self):
        handlerid = self.get_argument('handlerid','')
        del_handler_lib(self,handlerid)
        self.redirect('/permission/manage_list')


class AddUserRoleHandler(BaseHandler):
    """10为用户添加角色"""
    def post(self):
        userid = self.get_argument('userid','')
        roleid = self.get_argument('roleid','')
        add_user_role_lib(self,userid,roleid)
        self.redirect('/permission/manage_list')


class AddRolePermissionHandler(BaseHandler):
    """11为角色添加权限"""
    def post(self):
        roleid = self.get_argument('roleid','')
        permissionid = self.get_argument('permissionid','')
        add_role_permission_lib(self,roleid,permissionid)
        self.redirect('/permission/manage_list')


class DelFileHandler(BaseHandler):
    """12删除用户"""
    def get(self):
        uuid = self.get_argument('uuid','')
        del_user_lib(self,uuid)
        self.redirect('/permission/manage_list')


class AddUserDevRoleHandler(BaseHandler):
    """13添加用户到研发部门"""
    def post(self):
        userid = self.get_argument('userid','')
        roleid = self.get_argument('roleid','')
        add_user_dev_role_lib(self,userid,roleid)
        self.redirect('/permission/manage_list')


class DelUserRoleHandler(BaseHandler):
    """14为用户删除研发部门的角色"""

    @handler_permission('DelUserRoleHandler', 'handler')
    def get(self):
        userid = self.get_argument('userid','')
        roleid = self.get_argument('roleid','')
        print("********%s-----" % roleid)
        del_user_role_lib(self,userid,roleid)
        self.redirect('/permission/manage_list')


class DelUserOneRoleHandler(BaseHandler):
    """15为用户删除某个的角色"""

    def get(self):
        userid = self.get_argument('userid','')
        roleid = self.get_argument('roleid','')
        print("********%s-----" % roleid)
        del_user_for_one_role_lib(self,userid,roleid)
        self.redirect('/permission/manage_list')








