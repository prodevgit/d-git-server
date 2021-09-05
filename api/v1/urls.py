from django.urls import include, path

from api.v1 import views

urlpatterns = [
    #Auth APIS
    path('auth/create',views.UserCreateView.as_view(), name='user-create-api'),
    path('auth/login',views.LoginView.as_view(),name='user-login-api'),

    path('repository/create', views.RepositoryCreateView.as_view(), name='repository-create-api'),
    path('repository/list', views.RepositoryListView.as_view(), name='repository-list-api'),
    path('repository/accept-invite/<token>', views.RepositoryListView.as_view(), name='repository-accept-invite-api'),
    path('repository/<str:object_id>/detail', views.RepositoryDetailView.as_view(), name='repository-detail-api'),
    path('repository/<str:object_id>/addmember', views.RepositoryAddMemberView.as_view(), name='repository-addmember-api'),
]