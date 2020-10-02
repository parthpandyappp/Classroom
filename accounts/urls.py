from django.urls import path

from . import views

app_name = 'accounts'


urlpatterns = [
    path('profile/', views.profile),
    path('update-profile/', views.UserUpdatation, name='update'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout')
]
