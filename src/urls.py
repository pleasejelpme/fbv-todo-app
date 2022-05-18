from django.urls import path
from .views import home_view, detail_view, create_view, update_view, delete_view, login_view, logout_view, register_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('task/<int:pk>', detail_view, name='detail'),
    path('add-task/', create_view, name='create'),
    path('update-task/<int:pk>', update_view, name='update'),
    path('delete-task/<int:pk>', delete_view, name='delete'),
]