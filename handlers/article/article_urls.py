#coding=utf-8
from handlers.article.article_handler import (
    ArticleList,
    AddArticleHandler,
    AddCategoryTagHandler,
    DelCategoryTagHandler,
    ArticleContentHandler,
    AddCommentHandler,
    AddSecondCommentHandler,
    AddClickLikeHandler,
    ArticleSearch,
    ArticleModifyManageHandler,
    ArticleModifyHandler,
    ArticleDelHandler,
)


article_urls = [
    (r'/article/article_list/([0-9]{1,3})',ArticleList),
    (r'/article/add_article',AddArticleHandler),
    (r'/article/article_manage',AddCategoryTagHandler),
    (r'/article/del_category_tag',DelCategoryTagHandler),
    (r'/article/article',ArticleContentHandler),
    (r'/article/addcomment',AddCommentHandler),
    (r'/article/addsecondcomment',AddSecondCommentHandler),
    (r'/article/addlike',AddClickLikeHandler),
    (r'/article/search',ArticleSearch),
    (r'/article/article_modify_manage',ArticleModifyManageHandler),
    (r'/article/article_modify',ArticleModifyHandler),
    (r'/article/article_delete',ArticleDelHandler),
]