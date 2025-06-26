from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API endpoints
    path('api/comments/create/', views.create_comment, name='api_create_comment'),
    path('api/comments/<int:destination_id>/', views.get_comments, name='api_get_comments'),
    path('api/comments/delete/', views.delete_comment, name='api_delete_comment'),
    path('api/like/', views.handle_like, name='api_handle_like'),
] 