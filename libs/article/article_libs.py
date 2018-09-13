#coding=utf-8
from libs.flash.flash_lib import flash
from models.article.article_model import (
    Article,
    Comment,
    SecondComment,
    Tag,
    Category,
    UserLikeArticle,
)
from libs.pagination.pagination_libs import Pagination
from config import range_page


def article_list_lib(self,page):
    """01文章列表页"""
    articles = Article.order_by(Article.createtime.desc())
    comments = Comment.order_by(Comment.createtime.desc())
    tags = Tag.all()
    categorys = Category.all()
    # self.db.query(Article).order_by(args).all()
    page = int(page)
    items = self.db.query(Article).order_by(Article.createtime.desc()).slice((page -1) * range_page,page * range_page)

    pagination = Pagination(page,range_page,len(articles),items)

    return articles,comments,tags,categorys,pagination


def get_tags_categorys(self):
    """02返回添加文档的变量"""
    tags = Tag.all()
    categorys = Category.all()
    return tags, categorys


def add_article_lib(self,title,content,desc,category,tags,article_id):
    """02post请求添加文章"""
    if category is None:
        return {'status':False,'msg':'请选择分类'}
    if tags is None:
        return {'status':False,'msg':'请选择标签'}
    if desc is None:
        return {'status':False,'msg':'请输入摘要'}
    if title is None or content is None:
        return {'status':False,'msg':'请输入标题和文章内容'}

    if article_id:
        article = Article.by_id(article_id)
    else:
        article = Article()


    if article:
        article.title = title
        article.content = content
        article.desc = desc
        article.category_id = category
        for tag_id in tags:
            tag = Tag.by_id(tag_id)
            article.tags.append(tag)
        article.user_id = self.current_user.id
        self.db.add(article)
        self.db.commit()
    else:
        return {'status':False,'msg':'文档不存在'}
    if article_id:
        return {'status': True, 'msg': '文档修改成功'}
    return {'status':True,'msg':'文档添加成功'}


def add_category_tag_lib(self,category_name,tag_name):

    if tag_name:
        if Tag.by_name(tag_name) is not None:
            return {'status':False,'msg':'{}已存在'.format(tag_name.encode(encoding='UTF-8',errors='strict'))}
        tag = Tag()
        tag.name = tag_name
        self.db.add(tag)
        self.db.commit()
        return {'status': True, 'msg': '标签添加成功'}

    if category_name:
        if Category.by_name(category_name) is not None:
            return {'status':False,'msg':'{}已存在'.format(category_name.encode(encoding='UTF-8',errors='strict'))}
        category = Category()
        category.name = category_name
        self.db.add(category)
        self.db.commit()
        return {'status':True,'msg':'分类添加成功'}
    return {'status': False, 'msg': '请输入标签or分类'}


def del_category_tag_lib(self,c_uuid,t_uuid):
    """04删除便签或分类"""
    if c_uuid:
        category = Category.by_uuid(c_uuid)

        if category is None:
            flash(self, '分类不存在', 'error')
            return {'status':False}
        if category.articles:
            flash(self,'分类下面有文章，请先删除文章','error')
            return {'status': False}

        self.db.delete(category)
        self.db.commit()
        flash(self, '分类删除成功', 'success')
        return {'status':True}

    if t_uuid:
        tag = Tag.by_uuid(t_uuid)

        if tag is None:
            flash(self, '标签不存在', 'error')
            return {'status':False}
        if tag.articles:
            flash(self, '标签下面有文章，请先删除文章', 'error')
            return {'status': False}

        self.db.delete(tag)
        self.db.commit()
        flash(self, '标签删除成功', 'success')
        return {'status':True}
    flash(self, '请输入标签或分类', 'error')
    return {'status': False}


def article_content_lib(self,article_id):
    """05获取文章"""
    if article_id is None:
         return {'status':False,'msg':'缺少文章id'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status':False,'msg':'文章不存在'}
    article.readnum +=1
    self.db.add(article)
    self.db.commit()
    return {'status':True,'msg':'获取到文章','data':article}


def add_comment_lib(self,comment_content,article_id):
    """06获取文章并给它添加评论"""
    if comment_content and article_id:
        comment = Comment()
        comment.content = comment_content
        comment.user_id = self.current_user.id
        uuid = comment.uuid
        self.db.add(comment)
        self.db.commit()

        article = Article.by_id(article_id)
        if uuid:
            comment = Comment.by_uuid(uuid)
        if article and comment:
            article.comments.append(comment)
            self.db.add(article)
            self.db.commit()
            # print article.comments
            return {'status':True,'msg':'一级评论提交成功'}
        return {'status': False, 'msg': '文章或评论不存在'}
    return {'status':False,'msg':'文章或评论不存在'}



def add_second_comment_lib(self,comment_id,sec_comment_content):
    """07获取一级评论给其添加二级评论"""
    if comment_id and sec_comment_content:
        comment = Comment.by_id(comment_id)
        if comment:
            #先添加二级评论内容
            second_comment = SecondComment()
            second_comment.content = sec_comment_content
            second_comment.user_id = self.current_user.id
            self.db.add(second_comment)
            self.db.commit()
            #给一级评论添加二级评论
            comment.second_comments.append(second_comment)
            self.db.add(comment)
            self.db.commit()
            return {'status': True, 'msg': '二级评论提交成功'}
        return {'status': False, 'msg': '一级评论不存在'}
    return {'status': False, 'msg': '一级评论或二级评论内容不存在'}


def add_click_like_lib(self,article_id):
    """08给文章添加点赞关系"""
    if article_id:
        article = Article.by_id(article_id)
        user = self.current_user
        if article and user:
            if user in article.user_likes:
                article.user_likes.remove(user)
                self.db.add(article)
                self.db.commit()
                return {'status': False, 'msg': '点赞取消'}
            else:
                article.user_likes.append(user)
            self.db.add(article)
            self.db.commit()
            return {'status':True,'msg':'点赞成功'}
        return {'status':False,'msg':'文章或用户不存在'}
    return {'status':False,'msg':'文章不存在'}


def article_search_lib(self,category_id,tag_id):
    """09文章搜索"""
    articles = []
    category = Category.by_id(category_id)
    tag = Tag.by_id(tag_id)
    if category:
        articles = category.articles
    if tag:
        articles = tag.articles
    comments = Comment.order_by(Comment.createtime.desc())
    tags = Tag.all()
    categorys = Category.all()
    return articles, comments, tags, categorys


def article_modify_manage_lib(self):
    """10文档编辑管理"""
    articles =Article.order_by(Article.createtime.desc())
    categorys = Category.all()
    tags = Tag.all()
    return  articles,categorys,tags



def article_modify_lib(self,article_id):
    """11编辑文档"""
    article = Article.by_id(article_id)
    if article:
        categorys = Category.all()
        tags = Tag.all()
        return article,categorys,tags

def article_del_lib(self,article_id):
    """12文档删除"""
    article = Article.by_id(article_id)
    if article:
        self.db.delete(article)
        self.db.commit()
        return {'status':True,'msg':'文档删除成功'}
    return {'status':False,'msg':'文档不存在'}


