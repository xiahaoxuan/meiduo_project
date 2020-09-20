from . import views

from django.urls import path


urlpatterns = [
    path('orders/settlement/', views.OrderSettlementView.as_view(), name='settlement'),
    path('orders/commit/', views.OrderCommitView.as_view(), name='commit'),
    path('orders/success/', views.OrderSuccessView.as_view(), name='success'),
]