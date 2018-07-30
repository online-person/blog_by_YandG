from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^register/', views.user_register, name="register"),
    url(r'^check/', views.check_name),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^userinfo/', views.user_info, name='userinfo'),
    url(r'^activate/(.*)/', views.activate, name='activate'),

    # 帖子相关url
    url(r'^createpost/', views.create_post, name="createpost"),
    url(r'^delpost/(\d+)/',views.del_post,name="del_post"),
    url(r'^recoverypost/(\d+)',views.recovery_post,name="recoverypost"),
    url(r'^modifypost/(\d+)/',views.modify_post, name="modifypost"),
    url(r"^postlist/(\d+)/(\d+)", views.post_list, name="plist"),
    url(r"^postinfo/(\d+)/", views.post_info, name="postinfo"),
]