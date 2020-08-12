from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.ClassroomCreateView.as_view(), name='create'),
    path('join/<int:pk>/', views.ClassroomJoinView.as_view(), name="join"),
    path('processing/', views.processing, name="processing"),
    path('check/', views.check, name="check"),
    path('register/' ,views.register, name="register"),
]
