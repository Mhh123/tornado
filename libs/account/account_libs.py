#-*-coding:utf-8-*-
import json
import traceback
from models.account.account_user_model import User
from datetime import datetime
from random import choice
from string import printable
from uuid import uuid4
from libs.common.send_email.send_email_libs import send_qq_html_email

def edit_profile(self, name, password):
    if password == "":
        return {'status':False,'msg':'密码不能为空'}
    if name == "":
        return {'status':False,'msg':'用户名不能为空'}
    # user = User.by_name(name)
    # RequestHandler里面封装了current_user
    # @property
    # def current_user(self):
    user = self.current_user
    user.username = name
    user.password = password
    user.update_time = datetime.now()
    self.db.add(user)
    self.db.commit()
    return {'status':True,'msg':'修改成功'}

def send_email_libs(self,email):
    """发送邮件"""
    if email == '':
        return {'status':False,'msg':'邮箱不能为空'}

    email_code = ''.join([choice(printable[:62]) for i in xrange(4)])

    u = str(uuid4())

    text_dict = {
        u: self.current_user.id,
        'email_code': email_code
    }

    redis_dict = json.dumps(text_dict)
    self.conn.setex('email:%s'% email,redis_dict,500)

    content = """
        <p>html 邮件</p>
        <p><a href="http://mhh4399.com:8001/account/auth_email_code?code={}&email={}&user_id={}">点击绑定邮箱</a></p>
    """.format(email_code, email, u)

    send_qq_html_email("2937524077@qq.com",[email],"第一颗",content)

    return {'status':True,'msg':'邮箱发送成功'}


def auth_email_libs(self, email_code, email, u):
    """验证邮箱验证码"""
    redis_text = self.conn.get("email:%s"% email)
    if redis_text:

        text_dict = json.loads(redis_text)


        if text_dict and text_dict['email_code'] == email_code:
            user = self.current_user
            if not user:
                user = User.by_id(text_dict[u])
                # 为什么需要by_id呢？
                # 因为有可能用户永别的浏览器打开邮件，重新登陆，
                # 所以我们就获取不到current_user，需要by_id来重新获取到current_user

            user.email = email
            user.update_time = datetime.now()
            self.db.add(user)
            self.db.commit()
            return {'status':True,'msg':'邮箱修改成功'}
        return {'status':False,'msg':'邮箱验证码不正确'}
    return {'status':False,'msg':'邮箱验证码已过期,请重新绑定'}

def add_avatar_lib(self, avatar_data):
    """上传用户头像"""
    try:
        user = self.current_user
        user.avatar = avatar_data
        user.update_time = datetime.now()
        self.db.add(user)
        self.db.commit()
    except Exception as e:
        print(e)
        print("------------------------")
        print(traceback.format_exc())
        print("------------------------")
        send_qq_html_email(
            "2937524077@qq.com",
            ["2937524077@qq.com"],
            "第一颗",
            traceback.format_exc().replace('\n', '<br>')
        )
        return {'status':True,'msg':traceback.format_exc().replace('\n','<br>')}
    return {'status':True,'msg':'头像上传成功'}

