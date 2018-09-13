# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'DzAUqfPUn2XIQuev8V6P_Piv_Gupfla_SWvnaBfd'
secret_key = 'FQnVWzzu5L3VvkAmzshlKkkUQKwqYoPj4bBI7tc3'
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = '4399abc'


# 上传到七牛后保存的文件名


def upload_qiniu_file_content(content):
    """上传到七牛"""
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, None, content)
    return ret['key'], info  # 文件名， 状态信息


def down_qiniu_file(file_url):
    """从七牛下载"""
    # 或者直接输入url的下载方式
    base_url = file_url
    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=10)
    return private_url

# 要上传文件的本地路径
# localfile = './sync/bbb.jpg'

# print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)
