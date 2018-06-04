from django.conf.urls import url
import views

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^change-profile-pic/$', views.change_profile_pic, name='change_profile_pic'),
    url(r'^update-profile/$', views.update_profile, name='update_profile'),
]
