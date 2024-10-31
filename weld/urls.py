from django.urls import path

from . import views

app_name = 'weld'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_data, name='search'),
    path('weld_list/', views.weld_list, name='weld_list'),
    path('latest_data/', views.get_latest_data, name='get_latest_data'),
    path('ping_plc/', views.ping_plc, name='ping_plc'),
    path('weld/manage/', views.weld_manage, name='weld_manage'),
    path('search/download_excel/', views.download_excel, name='download_excel')
]
