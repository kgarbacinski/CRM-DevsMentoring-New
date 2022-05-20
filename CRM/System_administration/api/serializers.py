from rest_framework import serializers

from CRM_core.models import Path, Student, Mentor
from Meetings_calendar.models import Meeting


class AllMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mentor'] = instance.mentor.__str__()
        representation['student'] = instance.student.__str__()
        representation['path'] = instance.path.name
        representation['date'] = instance.date.strftime("%d-%m-%Y")
        return representation


class GetMeetingDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['year'] = int(instance.strftime("%Y"))
        representation['month'] = int(instance.strftime("%m"))
        representation['day'] = int(instance.strftime("%d"))
        return representation


class GetMentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.user.mentor.__str__()
        return representation


class GetStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.user.student.__str__()
        return representation


class GetPathsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Path
        fields = ['id', 'name']