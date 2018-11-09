django rest framework:
用户名:root
密码:root123456

1.在我们使用django rest framework进行登陆的时候,我们会报出错误,__str__ returned non-string (type NoneType)
就是说我们并未返回任何一个值.在这里我们需要对我们进行登录的用户界面进行改正.
将return name 改为return username就行.

2.使用序列化器进行反序列化的时候,需要对数据进行校验,才能获取验证成功的数据或者是保存成模型类
对象,在获取反序列化数据之前,必须调用is_valid()方法进行验证,验证成功返回True,否则返回false.

3.序列化:我们把变量从内存中变成可存储或者可传输的过程称之为序列化.
4.反序列化:把变量内容从序列化的对象重新读取到内存中称之为反序列化.

5.将我们的外键序列化成为一个id.

6.class Meta:
        model = Goods
        # 当我们指明之后,直接通过model做的映射,读取到这些字段的类型
        # 然后直接转化为serializer的field.
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = '__all__'


7.django的modelform可以自己定义字段,覆盖我们原有的字段.

8.当我们去继承任意一个view视图函数的话,都需要我们去重构这个get,否则我们的请求就不会被允许,
因为view会默认我们不允许该请求.重构如下:不写就报不被允许错误.
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
		
9.当我们不用ide软件自带的数据库的时候,都需要我们对settings里的数据库进行重新选择.实例如下:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "shop_city",
        'USER': 'root',
        'PASSWORD': "",
        'HOST': "127.0.0.1",
        'PORT': '3306'
    }
}

10.在我们使用generics.ListView时,只需要如此写,即可获取到所有数据
class GoodsListView(generics.ListAPIView):
    #
    # 商品列表页
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

11.我们已知的外键就是一种一对多的关系,一个主键下面,存在多个外键子例,
比如说A有一个外键字段B,那就是B的对象对应着A的每个实例对象,通过related_name
我们就可以获取到某个B实例下,所有的A实例对象.

12.在views里面写出如下所示内容,
class GoodsPagination(PageNumberPagination):
    page_size = 10
    # 下面page_query_param的p代表的是我请求的页数,
    page_query_param = 'p'
    # 而page_size_query_param中的page_size代表的是
    # 每页的条数
    page_size_query_param = 'page_size'
    max_page_size = 100
就可以代替settings里面我们配置的
# 进行分页功能的展示
# REST_FRAMEWORK ={
#     'PAGE_SIZE': 10,
# }

13.view视图函数的比较:
GenericViewSet(viewset):-drf
	GenericView-drf
		Apiview-drf
			view-dja
			
二者直接的区别主要是使用mixin进行区别
mixin
	createModelMixin
	ListmodelMixin 需要继承mixin这个东西,我们无法连接这些getlist方法,分页这些功能将会无法使用.
	updateModelMixin
	destoryMixin
	RetrieveModelMixin

viewsetMixin可以帮助我们实现绑定,需要绑定继承mixin.
viewset可以实现的绑定,就是继承了viewsetmixin.
将本应在代码中的绑定,移动到了url中进行绑定.
initialize_request,绑定了很多action,帮助我们动态serializer,

14.
django对我们的request和response进行了封装,也就是说浏览器对我们请求过来的数据进行了封装,request.parsing,就是对用户的数据进行了解析,比如说data,

request.data就是能够将post过来的数据,file放置到request.data里面,当我们再次请求的时候,就不需要在重复的get,post,直接从data里面获取.

query_params放的是我们get请求的参数,
parser解析用户发送过来的数据,json,或者是其他种类的数据格式,都能用这个去解析.

此处解释:
class GoodsFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    # 如果我们需要做模糊查询的时候,我们需要将lookup_expr='contains'
    # 如果想忽略大小写的话,我们需要在前面在加一个i,就是icontains.
    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']

16.
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
    page_size = 10
    # 下面page_query_param的p代表的是我请求的页数,
    page_query_param = 'p'
    # 而page_size_query_param中的page_size代表的是
    # 每页的条数
    page_size_query_param = 'page_size'

    max_page_size = 100


# GenericViewSet继承的是GenericApview
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # 商品列表页
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 当我们插上下面这条的时候,settings里面的内容就可以不再使用.
    pagination_class = GoodsPagination
    # 过滤条件的筛选
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filter_fields = ('name', 'shop_price')
    # 语法不支持fields和class在一起
    filter_class = GoodsFilter
    search_fields = {'name', 'goods_brief', 'goods_desc'}
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

1.drf的登录，点击登录出现登录界面，我们配置了login,logout,登录认证，防止跨站攻击，csrftoken自动注册
2.身份验证时将传入一组请求和一组标识凭据，相关联的机制，然后，权限和限制策略可以根据这些凭据来确定是否应该满足该请求。
3.身份验证是在视图的最开始，在发生权限和限制检查之前，以及允许任何其他代码继续运行。
4.身份验证本身是不允许传入请求的，它只是标识了请求需要的凭据。
5.sessionmiddleware和认证中间件，request请求进来，将session的id转换为user。
6.浏览器会自动设置cookie,并且将cookie带到我们的服务器。
7.用户认证重点在tokenauthentication。此身份是简单使用令牌验证，
就是说你携带着标识符进来，和存在的token令牌进行验证，

8.在installed_apps里面添加restframework.authtoken.进行数据库操作表，生成token表。一个用户里面存在一个token.













