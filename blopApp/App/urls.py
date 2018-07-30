from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/',views.index),
    url(r'^register/',views.user_register,name="register"),
    url(r'^check/',views.check_name),
    url(r'^post/list/', views.post_list),
    url(r'^post/create/', views.create_post),
    url(r'^post/edit/', views.edit_post),
    url(r'^post/read/', views.read_post),
    url(r'^post/search/', views.search),
]