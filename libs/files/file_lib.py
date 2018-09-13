# coding=utf-8
from datetime import datetime
from uuid import uuid4

import os

from config import range_page
from libs.pagination.pagination_libs import Pagination
from libs.qiniu.qiniu_libs import upload_qiniu_file_content, down_qiniu_file
from models.files.upload_file_mode import Files


def files_list_lib(self, page):
    """01返回文件"""
    page = int(page)
    files = self.current_user.files
    # print "files is :%s"%files
    # print files.all()
    # items = files.limit(range_page).offset((page - 1) * range_page)
    items = files.slice((page - 1) * range_page, page * range_page)
    # slice是切文章,可以参考源码
    # def slice(self, start, stop):
    # files和items都是查询语句，因为设置了惰性查找
    if page == 1 and items.count() < range_page:
        total = items.count()
    else:
        total = files.count()  # 该用户的总共文章

    return Pagination(page, range_page, total, items)
    # 返回的是Pagination类的实例


def upload_files_lib(self, upload_files):
    """02 上传文件"""
    # [{'body': '222ccc', 'content_type': u'text/plain', 'filename': u'6111.txt'},
    # {'body': '111aaaa', 'content_type': u'text/plain', 'filename': u'a.txt'}]
    # upload_files['filename']
    # upload_files['body']
    # upload_files['content_type']
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def save_file(self, upload_file):
    """ 03 保存单个文件"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}
    uuidname = str(uuid4()) + '.%s' % files_ext
    # 'sefaegaer.txt'   'sejfiajelgaeirf.jpg'
    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://127.0.0.1:9000/images/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(其实文件在硬盘上)', 'data': file_path}

    dirname = "images"
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    url = 'images/' + uuidname
    with open(url, 'wb') as f:
        f.write(file_content)

    file_name = upload_file['filename']
    files = Files()
    files.filename = file_name
    files.uuid = uuidname
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.update_time = datetime.now()
    files.file_hash = upload_file['body']
    # files.user_id = self.current_user.id
    files.users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://127.0.0.1:9000/images/' + files.uuid
    return {'status': True, 'msg': '文件保存成功', 'data': file_path}


def files_message_lib(self, uuid):
    """04返回文件"""
    files = Files.by_uuid(uuid)

    try:
        username = files.users[0].username
    except IndexError:
        username = files.files_users_del[0].username

    return files, username


def file_page_lib(self, page):
    """05 文件列表"""
    # 文件列表
    files = self.current_user.files
    page = int(page)
    items = files.slice((page - 1) * range_page, page * range_page)
    pagination = Pagination(page, range_page, files.count(), items)

    # 回收站文件列表
    files_del = self.current_user.users_files_del

    return pagination, files_del


def file_del_libs(self, uuid):
    """06删除文件"""
    file = Files.by_uuid(uuid)
    if file:
        try:
            user = self.current_user
        except Exception:
            print "nonexitence current_user"

        user.files.remove(file)
        # 从文件列表删除
        user.users_files_del.append(file)
        # 添加到回收站列表
        self.db.add(user)
        self.db.commit()

        # print "files_del type is :%s"% type(user.users_files_del)
        # print "files_del is :%s"% user.users_files_del

        return {'status': True, 'msg': '删除到回收站成功'}


def file_finaly_del_libs(self, uuid):
    """07彻底删除文件"""
    file = Files.by_uuid(uuid)
    if file:
        try:
            user = self.current_user
        except Exception as e:
            print "nonexitence current_user"

        # 从回收站列表删除
        user.users_files_del.remove(file)

        self.db.add(user)
        self.db.commit()
    return {'status': True, 'msg': '彻底删除成功'}


def file_rev_libs(self, uuid):
    """08恢复文件"""
    file = Files.by_uuid(uuid)
    if file:
        try:
            user = self.current_user
        except Exception as e:
            print "nonexitence current_user"

        # 添加到文件列表添加
        user.files.append(file)
        # 回收站列表中移除
        user.users_files_del.remove(file)

        self.db.add(user)
        self.db.commit()

    return {'status': True, 'msg': '恢复成功'}


def file_download_lib(self, uuid):
    """09文件下载"""
    # print os.path.dirname(__file__)#这个事当前正在操作的文件的路径(目录)
    # /home/pyvip/tornado_001/libs/files
    # print os.path.join(os.path.dirname(__file__),'test')
    # /home/pyvip/tornado_001/libs/files/test
    filepath = 'files/%s' % uuid
    # print filepath
    # files/659c794a-12d1-48b0-bb89-4ef7c6c640fa.jpg

    self.set_header('Content-Type', 'application/octet-stream')
    self.set_header('Content-Disposition', 'attachment; filename=%s' % uuid)
    with open(filepath, 'rb') as f:
        while True:
            dw = f.read(1024 * 5)  # 这个设置每次读多少
            if not dw:
                break

            self.write(dw)
            self.flush()

    self.finish()  # 记住要加finish


def upload_files_qiniu_lib(self, upload_files):
    """10 文件上传到七牛"""
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_qiniu_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def save_qiniu_file(self, upload_file):
    """ 11 保存单个文件到七牛"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}
    # 'sefaegaer.txt'   'sejfiajelgaeirf.jpg'

    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://p7bj6aatj.bkt.clouddn.com/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(其实文件在硬盘上)', 'data': file_path}

    # 上传到七牛
    print("=" * 80)
    ret, info = upload_qiniu_file_content(file_content)
    print("*" * 80)
    print ret
    print info
    if info.status_code != 200:
        return {'status': False, 'msg': '文件上传到七牛不正确', 'data': ''}

    files = Files()
    file_name = upload_file['filename']
    files.filename = file_name
    files.uuid = ret  # 保存的七牛返回到的文件名
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.update_time = datetime.now()
    files.file_hash = upload_file['body']
    # files.user_id = self.current_user.id
    files.users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://p7bj6aatj.bkt.clouddn.com/' + files.uuid
    return {'status': True, 'msg': '文件保存成功', 'data': file_path}


def download_files_qiniu_lib(self, uuid):
    """12 从下载文件"""
    if uuid == '':
        return {'status': False, 'msg': '没有文件ID'}
    old_file = Files.by_uuid(uuid)
    if old_file is None:
        return {'status': False, 'msg': '文件不存在'}
    qiniu_url = 'http://p7bj6aatj.bkt.clouddn.com/{}'.format(uuid)
    url = down_qiniu_file(qiniu_url)
    print(url)
    return {'status': True, 'data': url}
