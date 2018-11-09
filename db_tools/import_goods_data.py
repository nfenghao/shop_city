# -*- coding: utf-8 -*-
__author__ = 'ritian'
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
# 将整个项目的根目录加入到pyhton根目录之下
sys.path.append(pwd + "../")
# 单独使用django的model,需要进行配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_city.settings")

import django

# 调用这个函数
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]
    # filter不会报错,没啥问题,get会出现报错的问题的是.
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()