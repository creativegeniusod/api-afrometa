from django.urls import path, include

from . import views
from .DBOperations import DBOperations
from .LoginSettings import LoginSettings

urlpatterns = [
    path('', views.index, name='index'),
    path('user/login/action', views.loginAction, name='login_action'),
    path('user/logout', views.userLogout, name='user_logout'),
    path('users/', views.users, name='users'),
    path('user/save', views.userSave, name='user_save'),
    path('user/<slug:username>', views.userView, name='user_view'),
    path('user/edit/<slug:username>', views.userEdit, name='user_edit'),
    path('user/delete/<slug:username>/', views.userDelete, name='user_delete'),
    path('user/signup/', views.userSignUp, name='sign_up'),
    path('user/activate/', views.userActivate, name='user_activate'),
    path('user/permissions/', views.userPermissions, name='user_permissions'),
    path('user/permission/create/', views.userPermissionCreate, name='user_permission_create'),
    path('rooms/', views.listRooms, name='list_rooms'),
    path('page/votes/', views.pageVotes, name='page_votes'),
    path('charts/', include('charts.urls')),
    path('wallet/', views.wallet, name='page_wallet'),

    path('dbops/', DBOperations.index, name='db_operations_index'),
    path('dbops/purge/', DBOperations.purge, name='db_operations_action'),

    path('login/settings/', LoginSettings.index, name='login_settings_index'),
    path('login/settings/create/', LoginSettings.create, name='login_settings_create'),
    path('login/settings/<slug:id>/update/', LoginSettings.settingUpdate, name='login_setting_update'),

]
