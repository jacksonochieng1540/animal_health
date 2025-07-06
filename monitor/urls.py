
from django.urls import path
from monitor import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chart/temperature/', views.temperature_chart, name='temperature_chart'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),


]
