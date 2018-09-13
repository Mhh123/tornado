#-*-coding:utf-8-*-
from uuid import uuid4
from datetime import datetime
from string import  printable

from pbkdf2 import PBKDF2

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine,Column,Integer,String,
                         Text,Boolean,Date,DateTime,ForeignKey)
from libs.db.dbsession import Base,dbSession

from models.permission.permission_model import UserToRole
from models.article.article_model import Article
from models.files.upload_file_mode import Files,FilesToUser,DelFilesToUser

class User(Base):
    '''用户表'''
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)

    uuid = Column(String(36),unique=True,nullable=False,default=lambda:str(uuid4()))

    username = Column(String(50),nullable=False)
    _password = Column('password',String(64))
    createtime = Column(DateTime,default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)
    loginnum = Column(Integer,default=0)
    _locked = Column(Boolean,default=False,nullable=False)
    _avatar = Column(String(64))
    email = Column(String(50))
    mobile = Column(String(50))

    roles = relationship("Role", secondary=UserToRole.__table__)

    # 建立orm查询关系,与用户表和消息表的关系
    #  user_message = relationship("Message",secondary=Fike._table_)

    articles = relationship("Article",backref="user")
    comments = relationship("Comment",backref="user")
    second_comments = relationship("SecondComment",backref="user")
    # files = relationship("Files", backref="user",lazy="dynamic")
    files = relationship("Files", secondary=FilesToUser.__table__, lazy='dynamic')

    users_files_del = relationship("Files", secondary=DelFilesToUser.__table__)

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()
    @classmethod
    def by_id(cls,id):
        return dbSession.query(cls).filter_by(id=id).first()
    @classmethod
    def by_uuid(cls,uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(username=name).first()
    def __hash__password(self,password):
        return PBKDF2.crypt(password,iterations=0x2537)
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,password):
        # print(self.__hash__password(password))
        self._password = self.__hash__password(password)
    def auth_password(self,other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password,self.password)
        else:
            return False
    @property
    def avatar(self):
        return self._avatar if self._avatar else "default_avatar.jpeg"

    @avatar.setter
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)

        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):
                    os.unlink("static/images/useravatars/" + self._avatar)
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login,
        }


