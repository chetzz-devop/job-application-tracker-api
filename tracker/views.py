from datetime import date, timedelta
from rest_framework.views import APIView
from django.db.models import Count, Q
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from .models import JobApplication
from .serializer import JobSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class CreateJobApplication(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'company_name']
    search_fields = ['company_name', 'role']

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class EditDeleteApplication(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        applications = JobApplication.objects.filter(user=user)

        data = {
            "total_applied": applications.filter(status='applied').count(),
            "total_interviews": applications.filter(status='interview').count(),
            "total_rejected": applications.filter(status='rejected').count(),
            "total_offered": applications.filter(status='offered').count(),
            "total_applications": applications.count(),
        }

        return Response(data)


class UpcomingInterviewsView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        user = self.request.user
        today = date.today()
        upcoming = today + timedelta(days=2)

        return JobApplication.objects.filter(
            user=user,
            status='interview',
            interview_date__range=[today, upcoming]
        )
