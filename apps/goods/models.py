from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField


# Create your models here.

# 继承的是django的model
# 存在三个大类.比如说第一大类生鲜食品,和其下面的第二大类精品肉类,
# 还有其下面的第三大类比如说羊肉分类,牛肉类等等.几个类不是就要几张表
# 制定一个从属关系,使用一张表去控制所有类的级别


class GoodsCategory(models.Model):
    '''
    商品类别
    '''
    CATEGORY_TYPE = {
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    }
    # 名称
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    # 编码
    code = models.CharField(default='', max_length=30, verbose_name='类名code', help_text='类名code')
    # 简单描述
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    # choice 可选的,限制了该选项的字段值必须是所指定的choice中的一个.
    # 字段说明类别级别,
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    # 自己指向自己这张表,
    # 将第一大类和第二大类的商品级别放到一张表
    # 父类,使用'self'指向自己这张表,第二级别的父类.
    # 也可能存在none,因为第一大类没有父类
    # related_name:关联对象反向引用描述符,就是实现反向取值
    # 在django中,外键字段设置属性related_name,实现在serializers的时候可以通过属性值
    # 反向取出数据,

    # 我们已知的外键就是一种一对多的关系,一个主键下面,存在多个外键子实例,
    # 也就是说A如果有一个外键字段为B,那就是说,一个B对象可以对应多个A实例对象,
    # 那么通过设置related_name字段,就可以取得某个B实例下,所有的A实例对象.
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类目级别', help_text='父目录',
                                        related_name='sub_cat')
    # 判断是否将所有类别都放到tab中.
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''
    品牌名称
    '''
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name='商品类目')
    # 品牌名称
    name = models.CharField(default='', max_length=30, verbose_name='品牌名', help_text='品牌名')
    # 简单描述
    desc = models.TextField(default='', max_length=200, verbose_name='品牌描述', help_text='品牌描述')
    # 图片内容
    image = models.ImageField(max_length=200, upload_to='brands/')
    # default设置默认值,如果你没设置的话就是默认的,设置的话就是用你设置的.
    # 添加的时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        db_table = 'goods_goodsbrand'

    def __str__(self):
        return self.name


class Goods(models.Model):
    '''
    商品
    '''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品类目')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    name = models.CharField(max_length=100, verbose_name='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='商品库存')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品描述')
    goods_desc = UEditorField(verbose_name=u'内容', imagePath='goods/images/', width=1000, height=300,
                              filePath='goods/files/', default='')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='封面图')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    '''
    商品轮播图
    '''
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='images')
    image = models.ImageField(upload_to='', verbose_name='图片', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    '''
    轮播的商品
    '''
    goods = models.ForeignKey(Goods, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')

    class Meta:
        verbose_name = '商品轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='category', verbose_name='商品类目')
    goods = models.ForeignKey(Goods, related_name='goods')

    class Meta:
        verbose_name = '首页商品类别报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    '''
    热搜词商品
    '''
    keywords = models.CharField(default='', max_length=20, verbose_name='热搜词')
    index = models.IntegerField(default=0, verbose_name='排序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
