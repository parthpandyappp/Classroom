from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='click'),
    path('join/', views.JoinView.as_view(), name="join"),
    path('join-done/', views.JoinDoneView.as_view(), name="join-done"),
    path('processing/', views.processing, name="processing"),
    path('profile/', views.profile),
    path('update-profile/', views.UserUpdatation),
    path('register/', views.register, name="register"),
]
