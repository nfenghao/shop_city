"""shop_city URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf

    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from shop_city.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewset
# from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

# 生成router对象
router = DefaultRouter()
# 配置goods的url
# router自动帮助我们进行配置
router.register(r'goods', GoodsListViewSet, base_name='goods'),

# 配置category的url
router.register(r'categorys', CategoryViewset, base_name='categorys')

####################################
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',  # 这二者之间是互相绑定的关系
# })
######################################
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # media存储的是静态文件
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    ###########################################
    # 商品的列表页面(此处可隐去,当我们使用router)
    # url(r'goods/$', goods_list, name='goods-list'),
    ###########################################
    # 此处$符必须去,否则会爆炸
    url(r'docs/', include_docs_urls(title='shop_city')),
    # 在使用router时我们所需要进行的添加
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
