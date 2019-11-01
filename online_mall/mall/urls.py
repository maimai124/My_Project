from django.urls import path

from mall.views import index, login, register, user_center_info, user_center_manager, user_center_order, \
    user_center_browse, user_change, web_manage_user, user_add, web_manage_goods, goods_add, cancel

urlpatterns = [
    path('index/',index,name='index'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('user_center_info/',user_center_info,name='user_center_info'),
    path('user_center_manager/',user_center_manager,name='user_center_manager'),
    path('user_center_order/', user_center_order, name='user_center_order'),
    path('user_center_browse/', user_center_browse, name='user_center_browse'),
    path('user_change/', user_change, name='user_change'),
    path('user_add/', user_add, name='user_add'),
    path('web_manage_user/', web_manage_user, name='web_manage_user'),
    path('web_manage_goods/', web_manage_goods, name='web_manage_goods'),
    path('goods_add/', goods_add, name='goods_add'),
    path('cancel/', cancel, name='cancel'),
]