from django.urls import path, re_path

from . import views

urlpatterns = [
    path('carts/', views.CartsView.as_view(), name='info'),
]