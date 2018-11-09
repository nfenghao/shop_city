from rest_framework import serializers
from goods.models import Goods
from goods.models import GoodsCategory
from rest_framework.response import Response
from rest_framework import status


# 我们需要开始使用web ApI的第一件事是提供一种将代码段实例
# 序列化和反序列化为表示形式的方法json,我们可以通过声明
# 和django表单非常相似的序列化器serializer来完成操作,
# 在我们需要操作的app之下创建一个serializers.py文件,并且按照
# 如下这种添加方式from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
# class SnippetSerializer(serializers.Serializer):
#  id = serializers.IntegerField(read_only=True)
class CategorySerializer3(serializers.ModelSerializer):
    # 希望序列化category,
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    # 希望序列化category,因此我们需要设计一个序列化数据进行序列化处理,
    # 但是我们的类别不是一个,二十多个,所以我们需要添加一个属性:many = True
    # 这样我们就可以获取到所有的内容
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# django的modelform可以自己定义字段,覆盖我们原有的字段
class GoodsSerializer(serializers.ModelSerializer):
    # 当字段过于多,我们需要减轻工作量的时候,我们就可以引用modelserializer
    # 相当于是modelForm.
    # model能够新建一个序列化对象来影射这个model中的每个字段
    # 在返回的时候,并且当用户发送post请求的时候,可以直接通过serializers
    # 将这些内容保存在数据库中.和form差不多,但是serializers是专门用于
    # json中的.并且功能相当强大.
    # name = serializers.CharField(max_length=100, required=True)
    # click_num = serializers.IntegerField(default=0)
    # # 在这里展示图片时,serializer是会自动帮我们加上路径,/media/xxx
    # goods_front_image = serializers.ImageField()
    #
    # def create(self, validated_data):
    #     # objects相当于是我们model的管理器,objects中存在着一个create方法
    #     # 我们可以使用如下方法.将前端传递过来的数据,也就是我们的json数据
    #     # 比如给前端提供一个添加商品的接口的时候,需要这个goodsSerializer去验证
    #     # 我们这些数据的body.
    #     return Goods.objects.create(**validated_data)
    category = CategorySerializer()

    class Meta:
        model = Goods
        # 当我们指明之后,直接通过model做的映射,读取到这些字段的类型
        # 然后直接转化为serializer的field.
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = '__all__'
