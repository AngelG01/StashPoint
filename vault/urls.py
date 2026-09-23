from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('gallery/', views.gallery, name='gallery')
]