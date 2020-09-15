

from django.shortcuts import render
from django.views import View
from django import http

from goods.models import GoodsCategory
from contents.utils import get_categories

# Create your views here.


class ListView(View):
    def get(self, request, category_id, page_num):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('参数category_id不存在')
        categories = get_categories()
        context = {
            'categories': categories
        }
        return render(request, 'list.html', context=context)