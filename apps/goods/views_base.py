__author__ = 'ritian'
# 继承的是django的base.view
# 内建的展示视图:built-in display views
# 存在的部分
import json
from django.views.generic.base import View
from goods.models import Goods
from django.http import HttpResponse,JsonResponse
# 导入这个将某张表的所有字段进行序列化
from django.core import serializers


# from django.views.generic import ListView
# 使用上面的view和导入listview效果并无太大差异,
# 在这里我们使用View
# 首先我们先定义一个商品列表,来继承的是View
# 编写一个get方法,这样会默认传递一个request方法过来

class GoodsListView(View):
    def get(self, request):
        '''
        通过django的view实现
        商品的列表的展示页面
        :param request:
        :return:
        '''

        # 1.想展示商品列表,首先需要我们去取数据,此时需要导入
        # model中的Goods,通过orm查询将我们所需要的数据获取到
        # 2.格式如下只是为了获取到所有数据中
        # 获取到的数据是为了展示到前端,返回给json,所以说我们需要获取到
        # 商品的所有字段,转换成json格式,再返回
        # 3.由于我们获取到的是商品总数,因此我们需要建立一个列表
        # 通过这个列表将每个商品的字段放进去.获取到每个对象的每个字段
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            # 从django的forms中的models中导入model_to_dict
            # 通过这个东西能够将所有的字段进行序列化处理.
            from django.forms.models import model_to_dict
            #  serializers是一个module,不是一个函数或者方法,我们要是用的是
            # serializers里面的serialize方法,通过源码可以看出使用方法如下.
            json_data = serializers.serialize('json', goods)
            json_data = json.loads(json_data)
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
            # 在这里,由于数据库字段很多,我们只需要获取一部分
            # 观察演示结果就好,如下所示,获取到部分字段之后,
            # 我们可以将代表每个商品的部分属性的字典放置到
            # 我们创建的空列表json_list里面.
            # json_dict = {}
            # json_dict['name'] = good.name
            # json_dict['category'] = good.category.name
            # json_dict['market_price'] = good.market_price
            # json_list.append(json_dict)
        #####################################################
        # ###获取到上述数据,并且将这些数据传到json中,
        # ###我们可以使用到django里面的response去
        # ###上面所述的逐条读取的方法麻烦并且存在错误几率,因此我们采用简单的方法
        # ###能够直接将数据取出来的方法.如下:解释所用:
        # ###但是这样取数据依然会存在问题,就是某些不能序列化的东西单纯这样做
        # ###会报错,因此我们还需要使用另一种方法去解决这个问题
        #  from django.forms.models import model_to_dict
        #             json_dict = model_to_dict(good)
        #             json_list.append(json_dict)
        # 这句话的主要作用能够将我们的数据的字段转换成dict格式
        # 将列表中获取到的数据进行序列化
        # 返回json指明content_type的方式
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(json_data,safe=False)
        # return HttpResponse(json.dumps(json_data), content_type='application/json')
        # 在这步完成之后,我们将GoodsListView配置到我们的url里面
        # 在url中,设置一个访问到goods列表页的url,能够对我们从后端获取的数据
        # 进行展示,但是在前端会存在一个问题,就是现实的数据格式不是我们想要的格式
        # 在这里我们需要对获取到的数据格式进行处理.在这里我使用的jsonview插件
        # 这样展示出来的数据是符合规范的.
        # 这里使用的是列表的重载view,实现了数据的展示,既然这么简单,为什么还要用呢
        # 当我们将添加时间进行序列化的时候.会被报错,datetime is not json serialize
        # 而且这里面还会存在各种问题,需要我们使用restframework,比如说在图片展示的时候
        # 需要路径的指引,但是这些东西不需要我们去做,django已经主动帮助我们写好.
        #
