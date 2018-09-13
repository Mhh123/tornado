#coding=utf-8
from models.permission.permission_model import Role,Permission,Menu,Handler
from models.account.account_user_model import User
from libs.flash.flash_lib import flash

def permission_manage_list_lib(self):
    """01权限管理页面函数"""
    roles = Role.all()
    permissions = Permission.all()
    menus =Menu.all()
    handlers = Handler.all()
    users = User.all()
    # 研发员工
    dev_role = Role.by_name('研发部门')


    dev_users = dev_role.users if dev_role else []
    # print("*****")
    # print(type(dev_role))
    # print(dev_role)
    if dev_role is None:
        return roles, permissions, menus, handlers, users, dev_users,None
    return roles,permissions,menus,handlers,users,dev_users,dev_role.id

def add_role_lib(self,name):
    """02添加角色函数"""
    role = Role.by_name(name)
    if role is not None:
        flash(self, "角色不存在")
        return
    role = Role()
    role.name = name
    self.db.add(role)
    self.db.commit()
    flash(self, "角色添加成功", "success")


def del_role_lib(self,roleid):
    """03删除角色"""
    role = Role.by_id(roleid)
    if role is None:    #如果role是空的话，我们就什么也不操作
        flash(self,"角色不存在")
        return
    self.db.delete(role)
    self.db.commit()
    flash(self,"角色删除成功","success")

    # flash(self, "角色删除失败","error")

def add_permission_lib(self,name,strcode):
    """04添加权限"""
    permission = Permission.by_name(name)
    if permission is not None:
        return
    permission = Permission()
    permission.name = name
    permission.strcode = strcode
    self.db.add(permission)
    self.db.commit()
    flash(self, "权限添加成功", "success")


def del_permission_lib(self,permissionid):
    """05删除权限"""
    permission = Permission.by_id(permissionid)
    if permission is None:
        return

    self.db.delete(permission)
    self.db.commit()
    flash(self, "权限删除成功", "success")


def add_menu_lib(self,name,permissionid):
    """06添加菜单并为菜单添加权限"""
    permission = Permission.by_id(permissionid)
    menu = Menu.by_name(name)
    if permission is None:
        return
    if menu is None:
        menu = Menu()

    menu.name = name
    # print('**********')
    # print(type(menu))
    # print(menu)

    # print(type(permission))
    # print(permission)
    menu.permission = permission
    self.db.add(menu)
    self.db.commit()
    flash(self, "菜单权限添加成功", "success")



def del_menu_lib(self,menuid):
    """07为菜单删除权限"""
    # 其实这里只删除了menu，因为menu.permission这个对象是基于menu的
    # 所以只要删除了menu，那么基于它之上的都会被删除
    menu = Menu.by_id(menuid)
    if menu is None:
        return
    self.db.delete(menu)
    self.db.commit()
    flash(self, "菜单删除权限成功", "success")


def add_handler_lib(self,name,permissionid):
    """08为处理器添加权限"""
    permission = Permission.by_id(permissionid)
    handler = Handler.by_name(name)

    if permission is None:
        return

    if handler is None:
        handler = Handler()

    handler.name = name
    handler.permission = permission
    self.db.add(handler)
    self.db.commit()
    flash(self, "处理器权限添加成功", "success")


def del_handler_lib(self,handlerid):
    """09删除处理器"""
    handler = Handler.by_id(handlerid)
    if handler is None:
        return
    self.db.delete(handler)
    self.db.commit()
    flash(self, "处理器删除成功", "success")


def add_user_role_lib(self,userid,roleid):
    """10为用户添加角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.append(role) #注意这里画龙点睛
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户添加角色添加成功", "success")


def add_role_permission_lib(self,roleid,permissionid):
    """11为角色添加权限"""
    role = Role.by_id(roleid)
    permission = Permission.by_id(permissionid)
    if role is None or permission is None:
        return
    role.permissions.append(permission)
    self.db.add(role)
    self.db.commit()
    flash(self, "为角色添加权限添加成功", "success")


def del_user_lib(self,uuid):
    """12为用户删除角色"""
    user = User.by_id(uuid)
    if user is None:
        return
    user.roles = []
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户删除角色删除成功", "success")


def add_user_dev_role_lib(self,userid,roleid):
    """13添加用户到研发部门"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.append(role)
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户添加研发部门的角色添加成功", "success")


def del_user_role_lib(self,userid,roleid):
    """14为用户删除研发部门的角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    # print("********%s"%role)
    if user is None or role is None:
        return
    user.roles.remove(role)
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户删除研发部门的角色删除成功", "success")


def del_user_for_one_role_lib(self,userid,roleid):
    """15为用户删除某个角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    # print("********%s"%role)
    if user is None or role is None:
        return
    user.roles.remove(role)
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户删除某个角色删除成功", "success")












