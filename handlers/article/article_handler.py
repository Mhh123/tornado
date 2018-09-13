#coding=utf-8

import json
from handlers.base.base_handler import BaseHandler
from libs.article.article_libs import (
    article_list_lib,
    get_tags_categorys,
    add_article_lib,
    add_category_tag_lib,
    del_category_tag_lib,
    article_content_lib,
    add_comment_lib,
    add_second_comment_lib,
    add_click_like_lib,
    article_search_lib,
    article_modify_manage_lib,
    article_modify_lib,
    article_del_lib,
)

class ArticleList(BaseHandler):
    """01文章列表页"""
    def get(self,page):
        articles, comments, tags, categorys,pagination = article_list_lib(self,page)
        kw = {
            'articles':articles,
            'newarticles':articles[:3],
            'newcomments':comments[:3],
            'tags':tags,
            'categorys':categorys,
            'pagination':pagination,
        }
        return self.render('article/article_list.html',**kw)


class AddArticleHandler(BaseHandler):
    """02添加文档"""
    def get(self):
        tags, categorys = get_tags_categorys(self)
        kw = {'tags':tags,'categorys':categorys}
        return self.render('article/add_article.html',**kw)

    def post(self):
        title = self.get_argument('title',None)
        content = self.get_argument('article',None)
        desc = self.get_argument('desc',None)
        category = self.get_argument('category',None)
        tags = self.get_argument('tags',None)
        tags = json.loads(tags)
        article_id = self.get_argument('article_id',None)

        result = add_article_lib(self,title,content,desc,category,tags,article_id)
        if result['status'] == True:
            return self.write({'status':200,'msg':result['msg']})
        return self.write({'status':400,'msg':result['msg']})



class AddCategoryTagHandler(BaseHandler):
    """03文档管理"""
    def get(self):
        tags,categorys = get_tags_categorys(self)
        kw = {'tags':tags,'categorys':categorys}
        return self.render('article/article_add_category_tag.html',**kw)

    def post(self):
        category_name = self.get_argument('category_name','')
        tag_name = self.get_argument('tag_name','')
        result = add_category_tag_lib(self,category_name,tag_name)

        if result['status'] is True:
            return self.write({'status':200,'msg':result['msg']})
        return self.write({'status':400,'msg':result['msg']})


class DelCategoryTagHandler(BaseHandler):
    """04删除便签或分类"""
    def get(self):
        c_uuid = self.get_argument('c_uuid','')
        t_uuid = self.get_argument('t_uuid','')
        result = del_category_tag_lib(self,c_uuid,t_uuid)
        if result['status'] is True:
            return self.redirect('/article/article_manage')
        return self.redirect('/article/article_manage')


class ArticleContentHandler(BaseHandler):
    """05文档详情页"""
    def get(self):
        article_id = self.get_argument('id',None)
        result = article_content_lib(self,article_id)
        if result['status'] is True:
            article = result['data']
            comments = article.comments
            kw = {'article': article, 'comments':comments}
            return self.render('article/article.html',**kw)
        return result['msg']


class AddCommentHandler(BaseHandler):
    """06添加评论"""
    def post(self):
        comment_content = self.get_argument('content','')
        article_id = self.get_argument('id','')
        result = add_comment_lib(self,comment_content,article_id)
        if result['status'] is True:
            return self.write({'status':200,'msg':result['msg']})
        return self.write({'status':400,'msg':result['msg']})


class AddSecondCommentHandler(BaseHandler):
    """07添加二级评论"""
    def post(self):
        comment_id = self.get_argument('id',None)
        sec_comment_content = self.get_argument('content',None)
        result = add_second_comment_lib(self,comment_id,sec_comment_content)
        if result['status'] is True:
            return self.write({'status':200,'msg':result['msg']})
        return self.write({'status':400,'msg':result['msg']})


class AddClickLikeHandler(BaseHandler):
    """08给文章点赞"""
    def post(self):
        article_id = self.get_argument('article_id',None)
        result = add_click_like_lib(self,article_id)
        if result['status'] is True:
            return self.write({'status':200,'msg':result['msg']})
        return self.write({'status':400,'msg':result['msg']})


class ArticleSearch(BaseHandler):
    """09文章搜索"""
    def get(self):
        category_id = self.get_argument('category_id',None)
        tag_id = self.get_argument('tag_id',None)
        articles, comments, tags, categorys = article_search_lib(self,category_id,tag_id)

        kw = {
            'articles':articles,
            'newarticles':articles[:3] if len(articles)>2 else articles[:len(articles)],
            'newcomments':comments[:3] if len(comments)>2 else comments[:len(comments)],
            'tags':tags,
            'categorys':categorys,
        }
        return self.render('article/article_list.html',**kw)


class ArticleModifyManageHandler(BaseHandler):
    """10编辑文档管理"""
    def get(self):
        articles, categorys, tags = article_modify_manage_lib(self)
        kw = {
            'articles':articles,
            'categorys':categorys,
            'tags':tags,
        }
        return self.render('article/article_modify_manage.html',**kw)



class ArticleModifyHandler(BaseHandler):
    """11编辑文档"""
    def get(self):
        article_id = self.get_argument('id',None)
        article, categorys, tags = article_modify_lib(self,article_id)
        kw = {
            'article':article,
            'categorys':categorys,
            'tags':tags,
        }
        return self.render('article/article_modify.html',**kw)


class ArticleDelHandler(BaseHandler):
    """12删除文档"""
    def get(self):
        article_id = self.get_argument('id',None)
        result = article_del_lib(self,article_id)
        if result['status'] is True:
            return self.redirect('/article/article_modify_manage')






