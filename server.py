#-*-coding:utf-8-*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options, define
from config import settings
from handlers.main.main_urls import handlers
from models.account.account_user_model import User
from libs.db.dbsession import dbSession
from libs.db import create_talbes
from models.article import article_model
from models.files import upload_file_mode
# 有时候表创建不成功需要导入一下



define("port",default=9000,help="run port",type=int)
define("runserver",default=False,help="start server",type=bool)
define("t",default=False,help="create table",type=bool)
define("u",default=False,help="create user",type=bool)


if __name__ == '__main__':
    options.parse_command_line()
    if options.t:
        create_talbes.run()
    if options.u:
        user = User()
        user.username = 'xiaoming'
        user.password = 'qwe123'
        dbSession.add(user)
        dbSession.commit()
    if options.runserver:
        app = tornado.web.Application(handlers,**settings)#创建应用实例
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)    #监听9000端口
        print('start server...')
        tornado.ioloop.IOLoop.instance().start()  #启动服务

