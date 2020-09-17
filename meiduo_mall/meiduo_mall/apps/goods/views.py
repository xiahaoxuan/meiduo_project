from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django import http

from goods.models import GoodsCategory, SKU
from contents.utils import get_categories
from goods.utils import get_breadcrumb
# Create your views here.


# class DetailView(View):
#     def get(self, request, sku_id):
#         return render(request, 'detail.html')


class ListView(View):
    def get(self, request, category_id, page_num):
        # 接收参数
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('参数category_id不存在')
        sort = request.GET.get('sort', 'default')
        categories = get_categories()  # 获取商品分类
        breadcrumb = get_breadcrumb(category)  # 获取面包屑导航
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'
            sort_field = 'create_time'
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)
        # 创建分页器：每页N条记录
        paginator = Paginator(skus, 10)
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('Empty page')
        total_page = paginator.num_pages
        context = {
            'categories': categories,    # 频道分类
            'breadcrumb': breadcrumb,    # 面包屑导航
            'sort': sort,                # 排序字段
            'category_id': category_id,  # 第三级分类id
            'page_skus': page_skus,      # 分页后数据
            'page_num': page_num,        # 页数
            'total_page': total_page,    # 总页数
        }
        return render(request, 'list.html', context=context)