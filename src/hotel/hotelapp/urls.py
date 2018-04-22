# from django.conf.urls import url
from django.urls import path
from hotelapp import views


urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),

    path('create_hotel/', views.create_hotel, name='create_hotel'),
    path('update_hotel/<int:pk>/', views.update_hotel, name='update_hotel'),
    path('get_hotels/', views.get_hotels, name='get_hotels'),
    path('ajax_get_hotels/', views.ajax_get_hotels, name='ajax_get_hotels'),
    path('hotel/<slug:slug>/booking/', views.booking, name='booking'),
    # path('hotel/<slug:slug>/<int:year>/<int:month>/', views.hotel_details, name='hotel'),
    path('hotel/<slug:slug>/', views.hotel_details, name='hotel'),
]
