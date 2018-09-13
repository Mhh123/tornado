# coding=utf-8
from files_handler import (FilesTablelistHandler,
                           FilesUploadHandler,
                           FilesUploadQiniuHandler,
                           FilesMessageHandler,
                           FilesPageListHandler,
                           FilesDelHandler,
                           FilesFinalyDelHandler,
                           FilesRecoveHandler,
                           FilesDownloadHandler,
                           FileDownloadQiniuHandler,
                           )

files_urls = [
    (r'/files/filestable/list/([0-9]{1,3})', FilesTablelistHandler),
    (r'/files/files_upload/', FilesUploadHandler),
    (r'/files/files_upload_qiniu/', FilesUploadQiniuHandler),
    (r'/files/files_message', FilesMessageHandler),
    (r'/files/files_page/list/([0-9]{1,3})', FilesPageListHandler),
    (r'/files/files_delete', FilesDelHandler),
    (r'/files/files_delete_final', FilesFinalyDelHandler),
    (r'/files/files_recovery', FilesRecoveHandler),
    (r'/files/files_down', FileDownloadQiniuHandler),
]
