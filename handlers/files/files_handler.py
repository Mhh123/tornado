# coding=utf-8
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.web import gen

from handlers.base.base_handler import BaseHandler
from libs.files.file_lib import (files_list_lib,
                                 upload_files_lib,
                                 upload_files_qiniu_lib,
                                 files_message_lib,
                                 file_page_lib,
                                 file_del_libs,
                                 file_finaly_del_libs,
                                 file_rev_libs,
                                 file_download_lib,
                                 download_files_qiniu_lib,
                                 )


class FilesTablelistHandler(BaseHandler):
    """01显示文件列表"""

    def get(self, page):
        pagination = files_list_lib(self, page)

        # print "pagination.iter_pages() type is : %s"% type(pagination.iter_pages())
        # for i in pagination.iter_pages():
        #     print i
        # 带有 yield 的函数在 Python 中被称之为 generator（生成器）
        # pagination.iter_pages() type is: < type 'generator' >
        # 1
        # 2
        # 3
        # 4

        kw = {'pagination': pagination}
        return self.render('files/files_list.html', **kw)


class FilesUploadHandler(BaseHandler):
    """02上传文件"""

    def get(self):
        return self.render('files/files_upload.html')

    def post(self):
        upload_files = self.request.files.get('importfile', None)

        # upload_files type is <type 'list'>
        # [{'body': 'aaaaaaaaaaaaaaaaaa\r\n', 'content_type': u'text/plain',
        # 'filename': u'aaa.txt'},
        # {'body': 'bbbbbbbbbbbbbbbbbb\r\n', 'content_type': u'text/plain',
        # 'filename': u'bbb.txt'}]

        result = upload_files_lib(self, upload_files)

        if result is None:
            return self.write({'status': 400, 'msg': '出现错误'})
        return self.write({'status': 200, 'msg': '上传成功', 'data': result})


class FilesUploadQiniuHandler(BaseHandler):
    """02-2上传文件到七牛"""

    def get(self):
        return self.render('files/files_upload.html')

    def post(self):
        upload_files = self.request.files.get('importfile', None)
        result = upload_files_qiniu_lib(self, upload_files)

        if result is None:
            return self.write({'status': 400, 'msg': '出现错误'})
        return self.write({'status': 200, 'msg': '上传成功', 'data': result})


class FilesMessageHandler(BaseHandler):
    """03文件详情页"""

    def get(self):
        uuid = self.get_argument('uuid', None)
        files, username = files_message_lib(self, uuid)
        print "******"
        print "file.users is : %s" % username
        kw = {
            'files': files,
            'username': username,

        }
        return self.render('files/files_message.html', **kw)


class FilesPageListHandler(BaseHandler):
    """04文件分页列表"""

    def get(self, page):
        # 注意路由正则匹配的数字作为参数传递进来了users_files_del
        pagination, files_del = file_page_lib(self, page)
        kw = {
            'pagination': pagination,
            'files_del': files_del,
        }
        return self.render('files/files_page_list1.html', **kw)


class FilesDelHandler(BaseHandler):
    """05文件删除"""

    def get(self):
        uuid = self.get_argument('uuid')

        result = file_del_libs(self, uuid)
        if result['status'] is True:
            return self.redirect('/files/files_page/list/1')


class FilesFinalyDelHandler(BaseHandler):
    """06彻底删除文件"""

    def get(self):
        uuid = self.get_argument('uuid')

        result = file_finaly_del_libs(self, uuid)
        if result['status'] is True:
            return self.redirect('/files/files_page/list/1')


class FilesRecoveHandler(BaseHandler):
    """07恢复件"""

    def get(self):
        uuid = self.get_argument('uuid')

        result = file_rev_libs(self, uuid)
        if result['status'] is True:
            return self.redirect('/files/files_page/list/1')


class FileDownloadHandler(BaseHandler):
    """08文件下载"""

    def get(self):
        uuid = self.get_argument('uuid')
        file_download_lib(self, uuid)


class FileDownloadQiniuHandler(BaseHandler):
    """08-2 文件从七牛下载"""

    def get(self):
        uuid = self.get_argument('uuid', '')
        result = download_files_qiniu_lib(self, uuid)
        if result['status'] is True:
            return self.redirect(result['data'])
        else:
            return self.write(result['msg'])


class FilesDownloadHandler(BaseHandler):
    """09异步文件下载"""
    executor = ThreadPoolExecutor(2)

    @run_on_executor
    def file_download_libs(self, uuid):
        """08文件下载"""
        filepath = 'files/%s' % uuid
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % uuid)
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(1024 * 5)  # 这个设置每次读多少
                # print len(data)
                if not data:
                    break
                self.write(data)
                self.flush()
                # time.sleep(5)
        self.finish()  # 记住要加finish

    @gen.coroutine
    def get(self):
        uuid = self.get_argument('uuid')
        yield self.file_download_libs(uuid)
