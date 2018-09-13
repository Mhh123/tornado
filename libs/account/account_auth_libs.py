#-*-coding:utf-8-*-
from random import randint
from datetime import datetime
from utils.captcha.captcha import create_captcha
from models.account.account_user_model import User
from libs.yun_tong_xun.yun_tong_xun_lib import sendTemplateSMS
def create_captcha_img(self,pre_code,code):
    '''01生成验证码,把存到redis'''
    if pre_code:
        self.conn.delete("captcha:%s"%pre_code)
        # 注意你设置的redis.key是双引号就在delete()里面写双引号
    text,img = create_captcha()
    self.conn.setex('captcha:%s' % code, text,60)
    # setex设置一个redis并且过期时间

    return img
def auth_captcha(self, captcha_code=None, code=None):
    '''02-1校验验证码'''

    if captcha_code == '':
        return {'status':False,'msg':'请输入图形验证码'}
    elif self.conn.get('captcha:%s'% code).lower() != captcha_code.lower():
        return {'status':False,'msg':'输入的图形验证码不正确'}
    return {'status':True,'msg':'正确'}

def login(self, name, password):
    '''02登陆函数'''
    if name == '' and password == '':
        return {'status':False,'msg':'请输入用户名或密码'}
    user = User.by_name(name)
    if user and user.auth_password(password):
        user.last_login = datetime.now()
        user.loginnum+=1
        self.db.add(user)
        self.db.commit()
        self.session.set('user_name',user.username)
        return {'status':True,'msg':'登陆成功'}
    return {'status':False,'msg':'用户名或密码不正确'}

def get_mobile_code_lib(self, mobile, code, captcha):
    """03发送手机短信"""
    if isinstance(mobile,unicode):
        mobile = mobile.encode('utf-8')

    # if self.conn.get("captcha:%s"%code) != captcha:
    #     return {'status':False,'msg':'图形验证码不正确'}

    mobile_code = randint(1000,9999)
    self.conn.setex("mobile_code:%s"% mobile, mobile_code, 2000)
    print(mobile_code)
    # ---
    sendTemplateSMS(mobile,[mobile_code,30],1)
    return {'status':True,'msg': mobile}


def regist(self, mobile, mobile_captcha, name,
                        password1, password2, captcha, code,agree):
    print('------------------')
    print(mobile_captcha)
    print(captcha)
    print('------------------')
    if agree == "":
        return {'status':False,'msg':'请点击同意条款'}
    if self.conn.get("captcha:%s"%code) != captcha:
        return {'status':False,'msg':'图形验证码不正确'}
    if self.conn.get("mobile_code:%s"%mobile) != mobile_captcha:
        return {'status':False,'msg':'短信验证码不正确'}

    user = User.by_name(name)
    # print(type(user))
    # print(user)
    if name == "":
        return {'status':False,'msg':'用户名不能为空'}
    if user != None:
        return {'status':False,'msg':'用户已经存在'}
    if password1 != password2 and password1 != None:
        return {'status':False,'msg':'两次密码不一致'}
    #存入数据库
    user = User()
    user.username = name
    user.password = password2
    user.mobile = mobile
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': "注册成功"}







