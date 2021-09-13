from django.urls import include, path

from api.v1 import views

urlpatterns = [
    #Auth APIS
    path('auth/create',views.UserCreateView.as_view(), name='user-create-api'),
    path('auth/login',views.LoginView.as_view(),name='user-login-api'),

    path('repository/create', views.RepositoryCreateView.as_view(), name='repository-create-api'),
    path('repository/list', views.RepositoryListView.as_view(), name='repository-list-api'),
    path('repository/accept-invite/<object_id>/<token>/<operation>', views.RepositoryAcceptInviteView.as_view(), name='repository-accept-invite-api'),
    path('repository/<str:object_id>/detail', views.RepositoryDetailView.as_view(), name='repository-detail-api'),
    path('repository/<str:object_id>/addmember', views.RepositoryAddMemberView.as_view(), name='repository-addmember-api'),
    path('repository/clone', views.RepositoryCloneView.as_view(), name='repository-clone-api'),
    path('repository/push', views.RepositoryPushView.as_view(), name='repository-push-api'),
    path('repository/unauthorized-clone', views.RepositoryUnauthorizedCloneView.as_view(), name='repository-unauthorized-clone-api'),

    path('ssh/server-command-retreive',views.SSHServerCommandView.as_view(), name='ssh-command-retrieval-api'),

    path('branch/<str:object_id>/create',views.DGitBranchCreateView.as_view(), name='branch-create-api'),
    path('branch/<str:object_id>/detail',views.DGitBranchDetailView.as_view(), name='branch-detail-api'),
    path('branch/<str:object_id>/list',views.DGitBranchListView.as_view(), name='branch-list-api'),
]