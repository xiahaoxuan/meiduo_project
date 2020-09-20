from . import views

from django.urls import path, re_path


urlpatterns = [
    re_path(r'^payment/(?P<order_id>\d+)/$', views.PaymentView.as_view(), name='payment'),
]