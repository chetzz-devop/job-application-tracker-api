from django.contrib import admin
from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('job/', views.CreateJobApplication.as_view(), name='jobview'),
    path('job/<int:pk>/', views.EditDeleteApplication.as_view(),
         name='editdeleteapplication'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', views. DashboardView.as_view(), name='dashboard'),
    path('upcoming-interviews/', views.UpcomingInterviewsView.as_view(),
         name='upcoming-interviews'),


]
