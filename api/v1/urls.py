from django.urls import include, path

from api.v1 import views

urlpatterns = [
    #Auth APIS
    path('auth/create',views.UserCreateView.as_view(), name='user-create-api'),
    path('auth/login',views.LoginView.as_view(),name='user-login-api'),
  

]