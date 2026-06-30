from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):
    STATUSCHOICE = [
        ("applied", "applied"),
        ("interview", "interview"),
        ("offered", "offered"),
        ("rejected", "rejected")

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=400)
    role = models.CharField(max_length=400)
    status = models.CharField(choices=STATUSCHOICE, max_length=20)
    applied_date = models.DateField(auto_now_add=True)
    interview_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
