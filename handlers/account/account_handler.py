# -*-coding:utf-8-*-
from handlers.base.base_handler import BaseHandler
from libs.account.account_libs import (edit_profile,
                                       send_email_libs,
                                       auth_email_libs,
                                       add_avatar_lib,
                                       )


class ProfileHandler(BaseHandler):
    """用户信息函数"""

    def get(self):
        self.render('account/account_profile.html', message=None)


class ProfileEditHandler(BaseHandler):
    """编辑用户信息"""

    def get(self):
        self.render('account/account_edit.html')

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        result = edit_profile(self, name, password)
        if result['status'] is False:
            return self.render('account/account_profile.html', message=result['msg'])
        return self.render('account/account_profile.html', message=result['msg'])


class ProfileModifyEmailHandler(BaseHandler):
    """绑定邮箱"""

    def get(self):
        self.render('account/account_send_email.html')

    def post(self):
        email = self.get_argument('email')
        result = send_email_libs(self, email)
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])


class ProfileAuthEmailHandler(BaseHandler):
    """验证邮箱"""

    def get(self):
        email_code = self.get_argument('code', '')
        email = self.get_argument('email', '')
        u = self.get_argument('user_id', '')

        result = auth_email_libs(self, email_code, email, u)
        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])


class ProfileAddAvatarHandler(BaseHandler):
    """上传头像"""

    def post(self):
        avatar_data = self.request.files.get('user_avatar', '')

        # [{'body': 'aaaaaaaaaaaaaaaaaaa\r\n',
        #  'content_type': u'text/plain',
        #  'filename': u'aaa.txt'}]
        # self.write(avatar_data[0]['body'][:50])
        result = add_avatar_lib(self, avatar_data[0]['body'])

        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])
