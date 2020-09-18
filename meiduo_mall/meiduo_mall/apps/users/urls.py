from django.urls import path, re_path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('usernames/<username>/count/', views.UsernameCountView.as_view()),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9]{5,20})/count/$', views.UsernameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('info/', views.UserInfoView.as_view(), name='info'),
    path('emails/', views.EmailView.as_view(), name='emails'),
    path('emails/verification/', views.VerifyEmailView.as_view()),
    path('addresses/', views.AddressView.as_view(), name='address'),
    path('addresses/create/', views.AddressCreateView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDeleteAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    path('browse_histories/', views.UserBrowserHistory.as_view(), name='browse_histories'),
]
