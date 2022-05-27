import datetime

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from CRM_core.api.serializers import MeetingSerializer, ChangeStudentAvatarSerializer, \
    ChangeMentorAvatarSerializer, NoteSerializer
from CRM_core.models import Student, Mentor
from Meetings_calendar.models import Meeting, Note


class GetNoteText(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Note]:
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Note.objects.filter(author_id=user).filter(meeting_id=meeting)


class ListMeetingsByDates(generics.ListAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_date = timezone.make_aware(
            datetime.datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d %H:%M'),
            timezone.get_current_timezone())
        end_date = timezone.make_aware(datetime.datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d %H:%M'),
                                       timezone.get_current_timezone())
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Meeting.objects.filter(student__user=user).filter(date__range=[start_date, end_date]).order_by(
                'date')
        return Meeting.objects.filter(mentor__user=user).filter(date__range=[start_date, end_date]).order_by('date')


class ChangeAvatar(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return ChangeStudentAvatarSerializer
        else:
            return ChangeMentorAvatarSerializer

    def get_queryset(self, pk=None):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Student.objects.all()
        return Mentor.objects.all()
