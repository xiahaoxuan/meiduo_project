from django.urls import path, re_path

from . import views

urlpatterns = [
    path('carts/', views.CartsView.as_view(), name='info'),
    path('carts/selection/', views.CartSelectAllView.as_view(), name='selected'),
]