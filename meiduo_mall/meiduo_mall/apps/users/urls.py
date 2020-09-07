from django.urls import path, re_path


from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('usernames/<username>/count/', views.UsernameCountView.as_view()),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9]{5,20})/count/$', views.UsernameCountView.as_view())
]
