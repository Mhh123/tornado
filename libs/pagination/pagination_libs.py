#coding=utf-8
from math import ceil
class Pagination(object):

    def __init__(self,page,per_page,total,items):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items


    @property
    def pages(self):
        """总页pages=total/per_page"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))

        return pages


    @property
    def prev_num(self):
        """上一页"""
        if not self.has_prev:
            return None
        return self.page - 1


    @property
    def has_prev(self):
        return self.page > 1



    @property
    def next_num(self):
        """下一页"""
        if not self.has_next:
            return None
        return self.page + 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self,left_edge=1,left_current=1,right_edge=1,right_current=2):
        """
        :param left_edge:省略号左边显示几页
        :param left_current:当前页左边显示几页
        :param right_edge:
        :param right_current:
        :return:
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or\
                    (num > self.page - left_current -1 and
                     num < self.page + right_current) or \
                num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
        #干的事都是一样的，截取第几页~第几页，根据当前页显示页的范围
        #iter_pages函数呢是筛选生成一步到位
        # 我自己的方法呢是先生成后截取
        # total_page是一个列表【】[start:end]
        # 引入变量当前页current_page也就是你选中的哪一页，默认是1
        # start = current_page - 2 if current_page - 2 > 0 else 0
        # end = current_page + 3 if current_page + 3 < len(total_page) else len(total_page)
        # if end < 5:
        #     start = 0
        #     end = 5
        # elif end - start < 5:
        #     start = end - 5