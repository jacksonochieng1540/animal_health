
from django.urls import path
from monitor import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),  
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('chart/temperature/', views.temperature_chart, name='temperature_chart'),
    path('api/animals/', views.api_animals),
    path('api/records/', views.api_records),

]
