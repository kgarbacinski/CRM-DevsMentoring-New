from rest_framework import serializers

from CRM_core.models import Student, Mentor
from Meetings_calendar.models import Meeting, Note


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['mentor'] = instance.mentor.id
        representation['mentor_name'] = instance.mentor.__str__()
        # representation['student'] = instance.student.id
        representation['student_name'] = instance.student.__str__()
        # representation['path'] = instance.path.id
        representation['date'] = instance.date.strftime("%Y-%m-%d")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class ChangeStudentAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ChangeMentorAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'
