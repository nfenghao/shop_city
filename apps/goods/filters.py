from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    top_category = filters.NumberFilter(method='top_category_filter')

    # 如果我们需要做模糊查询的时候,我们需要将lookup_expr='contains'
    # 如果想忽略大小写的话,我们需要在前面在加一个i,就是icontains.
    def top_category_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name']
