from rest_framework import generics

from CRM_core.models import Mentor, Path, Student
from Meetings_calendar.models import Meeting
from System_administration.api.permissions import MentorAccess
from System_administration.api.serializers import (
    AllMeetingSerializer,
    GetPathsSerializer,
    GetStudentsSerializer,
    GetMeetingDatesSerializer,
    GetMentorsSerializer,
)


class ListAllMeetings(generics.ListAPIView):
    permission_classes = [MentorAccess]
    serializer_class = AllMeetingSerializer

    def get_queryset(self):
        query_list = Meeting.objects.all()
        user = self.request.user

        if user.groups.filter(name="Moderator").exists():
            mentor = self.request.query_params.get("mentor", None)
        else:
            mentor = Mentor.objects.get(user=user)

        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)
        day = self.request.query_params.get("day", None)
        student = self.request.query_params.get("student", None)
        path = self.request.query_params.get("path", None)

        if year:
            query_list = query_list.filter(date__year=year)
        if month:
            query_list = query_list.filter(date__month=month)
        if day:
            query_list = query_list.filter(date__day=day)
        if mentor:
            query_list = query_list.filter(mentor=mentor)
        if student:
            query_list = query_list.filter(student=student)
        if path:
            query_list = query_list.filter(path=path)
        return query_list.order_by("date")


class GetMeetingDates(generics.ListAPIView):
    serializer_class = GetMeetingDatesSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)

        if user.groups.filter(name="Moderator").exists():
            if year and month:
                return (
                    Meeting.objects.filter(date__year=year)
                    .filter(date__month=month)
                    .dates("date", "day")
                )
            if year:
                return Meeting.objects.filter(date__year=year).dates("date", "month")
            return Meeting.objects.dates("date", "year")

        if year and month:
            return (
                Meeting.objects.filter(mentor__user=user)
                .filter(date__year=year)
                .filter(date__month=month)
                .dates("date", "day")
            )
        if year:
            return (
                Meeting.objects.filter(mentor__user=user)
                .filter(date__year=year)
                .dates("date", "month")
            )
        return Meeting.objects.filter(mentor__user=user).dates("date", "year")


class GetMentorsList(generics.ListAPIView):
    serializer_class = GetMentorsSerializer

    def get_queryset(self):
        all_mentors = Meeting.objects.all()

        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)
        day = self.request.query_params.get("day", None)
        student = self.request.query_params.get("student", None)
        mentor = self.request.query_params.get("mentor", None)

        if year:
            all_mentors = all_mentors.filter(date__year=year)
        if month:
            all_mentors = all_mentors.filter(date__month=month)
        if day:
            all_mentors = all_mentors.filter(date__day=day)
        if student:
            all_mentors = all_mentors.filter(student_id=student)
        if mentor:
            all_mentors = all_mentors.filter(mentor_id=mentor)

        mentors_set = set(all_mentors.values_list("mentor_id"))

        mentors = [i[0] for i in list(mentors_set)]
        query_paths = Mentor.objects.filter(id__in=mentors)

        return query_paths


class GetStudentsList(generics.ListAPIView):
    serializer_class = GetStudentsSerializer

    def get_queryset(self):
        user = self.request.user
        all_meetings = Meeting.objects.all()

        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)
        day = self.request.query_params.get("day", None)
        student = self.request.query_params.get("student", None)

        if user.groups.filter(name="Moderator").exists():
            mentor = self.request.query_params.get("mentor", None)
        else:
            mentor = Mentor.objects.get(user=user)

        if year:
            all_meetings = all_meetings.filter(date__year=year)
        if month:
            all_meetings = all_meetings.filter(date__month=month)
        if day:
            all_meetings = all_meetings.filter(date__day=day)
        if student:
            all_meetings = all_meetings.filter(student_id=student)
        if mentor:
            all_meetings = all_meetings.filter(mentor_id=mentor)

        meetings_set = set(all_meetings.values_list("student_id"))

        paths = [i[0] for i in list(meetings_set)]
        query_paths = Student.objects.filter(id__in=paths)
        return query_paths


class GetPathsList(generics.ListAPIView):
    serializer_class = GetPathsSerializer

    def get_queryset(self):
        user = self.request.user
        all_meetings = Meeting.objects.all()

        year = self.request.query_params.get("year", None)
        month = self.request.query_params.get("month", None)
        day = self.request.query_params.get("day", None)
        student = self.request.query_params.get("student", None)
        if user.groups.filter(name="Moderator").exists():
            mentor = self.request.query_params.get("mentor", None)
        else:
            mentor = Mentor.objects.get(user=user)

        if year:
            all_meetings = all_meetings.filter(date__year=year)
        if month:
            all_meetings = all_meetings.filter(date__month=month)
        if day:
            all_meetings = all_meetings.filter(date__day=day)
        if student:
            all_meetings = all_meetings.filter(student_id=student)
        if mentor:
            all_meetings = all_meetings.filter(mentor_id=mentor)

        meetings_set = set(all_meetings.values_list("path__id"))

        paths = [i[0] for i in list(meetings_set)]
        query_paths = Path.objects.filter(id__in=paths)
        return query_paths
