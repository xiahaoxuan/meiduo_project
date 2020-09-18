from . import views

from django.urls import path, re_path

urlpatterns = [
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),
    re_path(r'^detail/(?P<sku_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^detail/visit/(?P<category_id>\d+)/$', views.DetailVisitView.as_view(), name='detail_visit')
]
