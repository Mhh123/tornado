# -*-coding:utf-8-*-

from handlers.base.base_handler import BaseHandler
from libs.account.account_auth_libs import (
    create_captcha_img,
    auth_captcha,
    login,
    get_mobile_code_lib,
    regist
)


class CaptchaHandler(BaseHandler):
    '''01生成图形验证码'''

    def get(self):
        pre_code = self.get_argument('pre_code', '')
        code = self.get_argument('code', '')

        img = create_captcha_img(self, pre_code, code)
        self.set_header('Content-Tpye', 'image/jpg')
        self.write(img)


class LoginHandler(BaseHandler):
    '''02登陆函数'''

    def get(self):
        self.render('account/auth_login.html')

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        captcha_code = self.get_argument('captcha', '')

        result = auth_captcha(self, captcha_code, code)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        # return self.write({'status':200,'msg':result['msg']})

        result = login(self, name, password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class MobileCodeHandler(BaseHandler):
    """03发送手机短信"""

    def post(self):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        # print(mobile)
        # print(code)
        # print(captcha)
        result = get_mobile_code_lib(self, mobile, code, captcha)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class RegistHandler(BaseHandler):
    """04注册函数"""

    def get(self):
        self.render("account/auth_regist.html", message='注册')

    def post(self):
        mobile = self.get_argument('mobile', '')
        mobile_captcha = self.get_argument('mobile_captcha', '')
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        captcha = self.get_argument('captcha', '')
        agree = self.get_argument('agree', '')
        # print('------------------')
        # print(mobile)
        # print(mobile_captcha)
        # print(code)
        # print(captcha)
        # print(name)
        # print(password1)
        # print(password2)
        # print('------------------')

        result = regist(self, mobile, mobile_captcha, name,
                        password1, password2, captcha, code, agree)

        print(result['msg'])
        if result['status'] == True:
            return self.redirect('user_login')
        return self.render('account/auth_regist.html', message=result['msg'])
