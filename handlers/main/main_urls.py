# -*-coding:utf-8-*-
from tornado.web import StaticFileHandler

from handlers.account.account_urls import account_urls
from handlers.article.article_urls import article_urls
from handlers.files.files_urls import files_urls
from handlers.message.message_urls import message_urls
from handlers.permission.permission_urls import permission_urls
from .main_handler import MainHandler

# static所有的静态文件都是通过这个StaticFileHandler类返回到前端页面的
handlers = [
    (r'/', MainHandler),
    (r'/images/(.*\.(jpg|mp3|mp4))', StaticFileHandler, {'path': 'files/'}),
]
handlers += account_urls  # 其实就是列表相加
handlers += permission_urls
handlers += article_urls
handlers += files_urls
handlers += message_urls
