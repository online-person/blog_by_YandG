from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/',views.index),
    url(r'^register/',views.user_register,name="register"),
    url(r'^check/',views.check_name),
    url(r'^login/',views.login,name='login'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^userinfo',views.user_info,name='userinfo'),
]