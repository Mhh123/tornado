#-*-coding:utf-8-*-

from handlers.base.base_handler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        # self.write('欢迎来到主页')
        self.redirect(r'/auth/user_login')
