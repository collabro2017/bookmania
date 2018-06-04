from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from polli import views as polli_views
from landing import views as landing_views
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views as rest_views


urlpatterns = [

    # Landing
    url('^', include('landing.urls')),

    # Publisher URLs
    url(r'^publisher/', include('publisher.urls')),

    # User URLs
    url(r'^user/', include('users.urls')),

    # Auth URLs
    url('^login/$', auth_views.login, name='login'),
    url('^login-complete/$', polli_views.login_complete, name='login-complete'),
    url('^register/$', polli_views.Register.as_view(), name='register'),

    url('^password-reset/$', auth_views.password_reset,
        {
            'template_name': 'registration/pwd_reset.html',
            'email_template_name': 'registration/pwd_reset_email.txt',
            'html_email_template_name': 'registration/pwd_reset_email.html',
            'subject_template_name': 'registration/pwd_reset_subject.txt'
         }, name='password_reset'),

    url('^password-reset-done/$', auth_views.password_reset_done, {'template_name': 'registration/pwd_reset_done.html'}, name='password_reset_done'),

    url('^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm,
        {'template_name': 'registration/pwd_reset_confirm.html'}, name='password_reset_confirm'),

    url('^password-reset-complete/$', auth_views.password_reset_complete, {'template_name': 'registration/pwd_reset_complete.html'}, name='password_reset_complete'),
    url('^logout/$', auth_views.logout, name='logout'),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),

    # SCHEMA
    url(r'^schema/$', get_schema_view(title='API')),

    # Admin
    url(r'^admin/', admin.site.urls),
]