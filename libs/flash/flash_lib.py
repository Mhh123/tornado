#coding=utf-8

def flash(self,message,category='message'):
    """先在代码里调用flash"""
    flashes = self.session.get('_flashes',[])
    flashes.append((category,message))  #[('error','保存失败'),('sucess','分类保存了')]
    self.session.set('_flashes',flashes)


def get_flashed_messages(self,with_categories=False,category_filter=[]):
    """后在在html页面调用get_flashed_messages"""
    flashes = self.flashes
    if flashes is None:
        self.falshes = flashes = self.session.get('_flashes',[])
        del self.session['_flashes']
    if category_filter:
        flashes = list(filter(lambda f: f[0] in category_filter,flashes))

    if not with_categories:
        return [x[1] for x in flashes]

    # 非常复杂相当于异步，flashes这个值在不断的变化
    # 在某个时刻或者说某个阶段，返回值是flashes
    # 真正处理数据还是在falsh()也就是服务器，不会在html页面
    # 只是在html页面调用了get_flashed_messages
    # 所以说还是服务器处理了数据
    return flashes


#在html写消息闪现的时候必须放在最上面，准确的说需要放的位置之前不能有其他的内容

#html页面代码与flask相同
#普通闪现
# {% for message in get_flashed_messages() %}
#     <p style="background-color: #bce8f1">{{ message }}</p>
# {% end %}
#
# 分类闪现
# {% for  category, message in get_flashed_messages(with_categories=True) %}
#     {% if category == 'error' %}
#         <p style="background-color: red">{{ message }}</p>
#     {% elif category == 'success'%}
#         <p style="background-color: green">{{ message }}</p>
#     {% end %}
# {% end %}

#过滤闪现
# <!--  过滤闪现 -->
#        {% for  message in get_flashed_messages(category_filter=["error"]) %}
#            <p style="background-color: red">{{ message }}</p>
#        {% end %}
#
#        {% for  message in get_flashed_messages(category_filter=["success"]) %}
#            <p style="background-color: #bce8f1">{{ message }}</p>
#        {% end %}

#弹窗
# {% for category, message in get_flashed_messages(with_categories=True) %}
#       {% if category == 'error' %}
#           <script type = "text/javascript" >
#               swal({
#                 'title': '错误',
#                 'text': '{{ message }}',
#                 'type': 'error',
#                 'showCancelButton': false,
#                 'showConfirmButton': false,
#                 'timer': 2000,
#                 })
#           </script >
#       {% elif category == 'success' %}
#          <script type = "text/javascript" >
#                swal({
#                     'title': '正确',
#                     'text': '{{ message }}',
#                     'type': 'success',
#                     'showCancelButton': false,
#                     'showConfirmButton': false,
#                     'timer': 2000,
#                     })
#          </script >
#       {% end %}
# {% end %}