from . import views

from django.urls import path


urlpatterns = [
    path('qq/login/', views.QQAuthURLView.as_view()),
    path('oauth_callback/', views.QQAuthUserView.as_view()),
]