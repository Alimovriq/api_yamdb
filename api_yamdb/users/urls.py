from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('api/v1/', include('api.urls')),
]
