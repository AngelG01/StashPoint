from django.contrib.auth import views as auth_view
from django.urls import path 
from .views import sign_up

app_name = 'accounts'

urlpatterns = [
    path('login', auth_view.LoginView.as_view(), name='login'),
    path('logout', auth_view.LogoutView.as_view(), name='logout'),
    path('sign_up', sign_up, name='sign_up')

]