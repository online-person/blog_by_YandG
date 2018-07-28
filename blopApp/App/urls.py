from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/',views.index),
    url(r'^register/',views.user_register,name="register"),
    url(r'^check/',views.check_name),
]