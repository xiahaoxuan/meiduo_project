# 系统的
from collections import OrderedDict
# django
from django.shortcuts import render
from django.views import View
# 自定义
from contents.models import ContentCategory
from contents.utils import get_categories


class IndexView(View):
    """首页广告"""
    def get(self, request):
        """提供首页广告界面"""
        categories = get_categories()
        # 查询首页广告数据
        # 查询所有的广告类别
        content_categories = ContentCategory.objects.all()
        contents = OrderedDict()
        for content_category in content_categories:
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')

        # 使用广告类别查询出该类别对应的所有的广告内容

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)


