from django.shortcuts import render
from .serializers import GoodsSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters
# 这个response是drf的response对象,封装了response和
# request对象
from rest_framework.response import Response
# Create your views here.
from .models import Goods, GoodsCategory


# 如下是关于分页进行的一些diy
class GoodsPagination(PageNumberPagination):
    page_size = 12
    # 下面page_query_param的p代表的是我请求的页数,
    page_query_param = 'page'
    # 而page_size_query_param中的page_size代表的是
    # 每页的条数
    page_size_query_param = 'page_size'

    max_page_size = 100


# GenericViewSet继承的是GenericApview
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页，分页，搜索，过滤，排序
    '''
    # 商品列表页
    # 这里面分别实现了分页，搜索，过滤，排序等功能
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 当我们插上下面这条的时候,settings里面的内容就可以不再使用.
    pagination_class = GoodsPagination
    # 过滤条件的筛选
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    # 语法不支持fields和class在一起
    filter_class = GoodsFilter
    # 可以添加的筛选条件，通过这些条件我们能够查到所有和我们关键字相关的。
    # 并且这里面可以添加一些正则表达式来进行模糊查询。
    # 譬如说：‘’'^'开始 - 搜索。
    # '='完全匹配。
    # '@'全文搜索。（目前只支持Django的MySQL后端。）
    # '$'正则表达式搜索。
    search_fields = {'name', 'goods_brief', 'goods_desc'}
    ordering_fields = {'sold_num', 'shop_price'}
    ##########################
    # class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    ########################################
    # 这是apiview的版本
    # def get(self, request, format=None):
    #     goods = Goods.objects.all()
    #     # GoodsSerializer直接对goods进行序列化处理
    #     # many的配置表示我们是一个list对象,不是queryset对象
    #     # 我们是单个good的话,我们就不用配置这个.
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #     return Response(goods_serializer.data)  # 这里面的data就是我们serializer
    #     # 之后的数据

    # def post(self, request):
    #     # 这里面我们使用的是drf的restframework的request,并不是d的request
    #     # 在django的request中并不存在request.data,drf中对request,response进行封装
    #     # 因此说,我们可以使用drf进行request.data的获取,使用drf进行数据获取就变得很简单,
    #     # 无论传输数据的方式是什么,都可以一并获取到,放置到data中.
    #     #
    #     serializer = GoodsSerializer(data=request.data)
    #
    #     # 在使用反序列化的数据之前,必须使用is_valid()进行数据校验.
    #     if serializer.is_valid():
    #         serializer.save()
    #         # save会调用serializer的create方法.
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 提供了简单的过滤功能:
    # 这里面存在了对返回内容的筛选的get_queryset等功能


# ///////////////////////////////////////////////////
# 当我们添加上filter_backends = (DjangoFilterBackend,)之后,
# 下面代码就可以去掉了:
# def get_queryset(self):
#     # 获取前端传递过来的数据
#     queryset = Goods.objects.all()
#     price_min = self.request.query_params.get('price_min', 0)
#     if price_min:
#         queryset = queryset.filter(shop_price__gt=int(price_min))
#         return queryset
#
#     return Goods.objects.filter(shop_price__gt=100)
# /////////////////////////////////////////////////////////////////////////////////

# mixins.RetrieveModelMixin是让我们能看到商品的详情页.
# 在以前的工作中,我们未来获取到列表的详情页,我们需要自己编写
# 一系列的正则表达式来匹配比如说
# url(r'^(?P<id>[0-9]+)/$'),但是当我们使用drf之后,只需要我们在里面引入
# mixins.RetrieveModelMixin就行了.drf
class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    List:
            商品分类列表数据
    '''
    # 在商品的分类中,展示给我们的界面往往是包含层次感的,所以说,
    # 我们在drf中,也需要我们进行级别构造.那么我们该如何展示出层次感呢
    # 我们需要进行serializer的改变.
    # 那么我们该如何去实现单纯实现某一个类别下面的具体内容呢?
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
