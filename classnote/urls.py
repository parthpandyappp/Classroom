from django.urls import path

from . import views

app_name = 'classnote'


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='click'),
    path('join/', views.JoinView.as_view(), name='join'),
    path('processing/', views.processing, name='processing'),
    path('okay/', views.JoinOkayView.as_view(), name='okay')
]
