from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Document, Subject, Topic


class DocumentSerializer(serializers.ModelSerializer):
    subtopic_name = serializers.CharField(
        read_only=True, source="topic.name")
    subtopic_description = serializers.CharField(
        read_only=True, source="topic.description")

    class Meta:
        model = Document
        fields = ['name', 'file', 'type',
                  'subtopic_name', 'subtopic_description']


class AccessToFileSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('has_access')
    subtopic_name = serializers.SerializerMethodField('get_subtopic_name')

    def has_access(self, obj) -> bool:
        topic = self.context.get('topic')
        user = User.objects.get(id=obj.id)
        users_set = topic.user.all()
        return user in users_set

    def get_subtopic_name(self, obj) -> Topic:
        subtopic = self.context.get('topic')
        return subtopic.name

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'access', 'subtopic_name']


class AccessToSubjectSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('has_access')
    subject_name = serializers.SerializerMethodField('get_subtopic_name')

    def has_access(self, obj) -> bool:
        subject = self.context.get('subject')
        topics = Topic.objects.filter(subject=subject).all()
        if not topics:
            return False
        user = User.objects.get(id=obj.id)

        for topic in topics:
            users_set = topic.user.all()
            if user not in users_set:
                return False

        return True

    def get_subtopic_name(self, obj) -> Subject:
        subject = self.context.get('subject')
        return subject.name

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'access', 'subject_name']


class UserSearchBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
