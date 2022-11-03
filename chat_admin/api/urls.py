from django.urls import path

from . import views

urlpatterns = [
    path('user/create', views.createUser, name='api_create_user'),
    path('create/user', views.createUser, name='api_create_user_1'),
    path('user/<slug:username>', views.userLookup, name='user_lookup'),
    path('search/user', views.userSearch, name='user_search'),
    path('create/room', views.createRoom, name='create_room'),
    path('room/message', views.saveRoomMessage, name='save_room_message'),
    path('add/new/room/users', views.addNewUsers, name='add_new_users'),
    path('get/room/messages', views.getRoomMessages, name='get_room_messages'),
    path('page/room/', views.pageRoom, name='page_room'),
    path('vote/<slug:vote>', views.castSiteVote, name='site_vote'),
    path('vote/page/score/', views.getPageScore, name='get_page_score'),
    path('wallet/', views.getWalletInfo, name='get_wallet_info'),
    path('user/wallet/', views.getUserWalletInfo, name='get_user_wallet_info'),
    path('wallet-status/', views.walletStatus, name='get_or_post_wallet_status'),
    path('wallet-whitelist-add/', views.walletAddWhitelist, name='add_whitelist_to_wallet'),
    path('wallet-whitelist-remove/', views.walletRemoveWhitelist, name='remove_whitelist_to_wallet'),
    path('sign/options/', views.getSignOptions, name='get_sign_in_up_options'),
]
