import datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from CRM_core.models import Student, Path, Mentor
from .permissions import MentorCreate
from .serializers import NoteSerializer, EditDeleteNoteSerializer, MeetingDetailSerializer, AddMeetingSerializer, \
    MeetingSerializer, StudentsSerializer
from ..models import Note, Meeting


class ListNotes(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_class = IsAuthenticated

    def get_queryset(self) -> QuerySet[Note]:
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Note.objects.filter(author_id=user).filter(meeting_id=meeting)


class EditDeleteNote(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditDeleteNoteSerializer
    permission_class = IsAuthenticated

    def get_queryset(self, pk=None):
        return Note.objects.all()

    def perform_update(self, serializer):
        serializer.save()


class MeetingDetail(generics.ListAPIView):
    serializer_class = MeetingDetailSerializer

    def get_queryset(self):
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user).filter(id=meeting)


class ListMeetings(generics.ListAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Meeting.objects.filter(student__user=user).filter(date__year=year)\
                .filter(date__month=month).order_by('date')
        return Meeting.objects.filter(mentor__user=user).filter(date__year=year).filter(date__month=month)\
            .order_by('date')


class AddMeeting(generics.CreateAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

    def perform_create(self, serializer):
        data = self.request.data
        mentor = data['mentor']
        student = data['student']
        date = timezone.make_aware(datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
                                   timezone.get_current_timezone())
        path_id = Student.objects.get(id=student).path.id
        meeting = serializer.save(
            date=date,
            mentor=Mentor.objects.get(id=mentor),
            student=Student.objects.get(id=student),
            path=Path.objects.get(id=path_id))
        Note.objects.create(
            meeting=meeting,
            author=User.objects.get(id=Mentor.objects.get(id=data['mentor']).user.id),
            title='',
            text=data['note'] if 'note' in data else '')
        Note.objects.create(
            meeting=meeting,
            author=User.objects.get(id=Student.objects.get(id=data['student']).user.id),
            title='',
            text='')


class EditDeleteMeeting(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

    def perform_update(self, serializer):
        data = self.request.data
        meeting_id = data['id']
        student_id = data['student']
        date = timezone.make_aware(datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
                                   timezone.get_current_timezone())
        path_id = Student.objects.get(id=student_id).path.id
        serializer.save(
            id=meeting_id,
            date=date,
            student=Student.objects.get(id=student_id),
            path=Path.objects.get(id=path_id))

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user)


class ListStudents(generics.ListAPIView):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(mentor__user__username=user)
