from CRM_core.models import Mentor
from rest_framework import serializers

from ..models import Meeting, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["date"] = instance.meeting.date.strftime("%d-%m-%Y")
        representation["hour"] = instance.meeting.date.strftime("%H:%M")
        representation["student"] = instance.meeting.student.__str__()
        representation["mentor"] = instance.meeting.mentor.__str__()
        return representation


class EditDeleteNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["meeting"] = instance.meeting.id
        return representation


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["date"] = instance.date.strftime("%Y-%m-%d")
        representation["hour"] = instance.date.strftime("%H:%M")
        return representation

    class Meta:
        model = Meeting
        fields = "__all__"


class AddMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["student"] = instance.user.student.__str__()
        representation["email"] = instance.user.email
        representation["enrolment"] = instance.user.student.enrollmentDate.strftime(
            "%Y-%m-%d"
        )
        representation["path"] = instance.user.student.path.name
        return representation
