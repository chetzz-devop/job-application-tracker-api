from rest_framework import serializers
from .models import JobApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'user', 'role', 'company_name', 'status',
                  'interview_date', 'applied_date', 'notes']

    def validate(self, data):
        interview_date = data.get('interview_date')
        status = data.get('status')

        if interview_date and status != 'interview':
            raise serializers.ValidationError(
                "If interview_date is set, status must be 'interview'."
            )

        if status == 'interview' and not interview_date:
            raise serializers.ValidationError(
                "If status is 'interview', interview_date must be set."
            )

        return data
