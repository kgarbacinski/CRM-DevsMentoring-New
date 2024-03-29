import enum
import re
from typing import Dict, Tuple, Union

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import Document, Subject, Topic
from .permissions import FileAccessPermission
from .serializers import (
    AccessToFileSerializer,
    AccessToSubjectSerializer,
    DocumentSerializer,
    UserSearchBoxSerializer,
)


class Patterns:
    whole_name_pattern = r"\w+\s\w+"


class DocumentView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Document]:
        subtopic_id = self.kwargs["pk"]
        try:
            topic = Topic.objects.get(id=subtopic_id)
        except Topic.DoesNotExist:
            raise Http404
        users = topic.user.all()
        if (
            self.request.user in users
            or self.request.user.is_superuser
            or self.request.user.groups.filter(name="Mentor").exists()
        ):
            documents = Document.objects.filter(topic_id=subtopic_id).all()
            if not documents:
                raise Http404
            return documents
        raise PermissionDenied


class HasAccessToFileView(
    generics.ListAPIView, mixins.DestroyModelMixin, mixins.CreateModelMixin
):
    serializer_class = AccessToFileSerializer
    permission_classes = [FileAccessPermission]
    queryset = User.objects.filter(groups__name="Student").all()

    def get_serializer_context(self) -> Dict[str, Union[None, Request, GenericAPIView]]:
        context = super().get_serializer_context()
        subtopic_id = self.kwargs["pk"]
        try:
            topic = Topic.objects.get(id=subtopic_id)
        except Topic.DoesNotExist:
            raise Http404
        context["topic"] = topic
        return context

    def __get_subtopic_and_user(
        self, subtopic_id, user_id
    ) -> Union[Response, Tuple[Topic, User]]:
        if not subtopic_id or not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            topic = Topic.objects.get(id=subtopic_id)
            user = User.objects.get(id=user_id)
        except (Topic.DoesNotExist, User.DoesNotExist):
            raise Http404
        return topic, user

    def post(self, request, *args, **kwargs) -> Response:
        subtopic_id = self.kwargs["pk"]
        user_id = request.data
        topic, user = self.__get_subtopic_and_user(subtopic_id, user_id)
        topic.user.add(user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        subtopic_id = self.kwargs["pk"]
        user_id = request.data
        topic, user = self.__get_subtopic_and_user(subtopic_id, user_id)
        topic.user.remove(user)
        return Response(status=status.HTTP_200_OK)


class HasAccessToSubjectView(
    generics.ListAPIView, mixins.DestroyModelMixin, mixins.CreateModelMixin
):
    serializer_class = AccessToSubjectSerializer
    permission_classes = [FileAccessPermission]
    queryset = User.objects.filter(groups__name="Student").all()

    def __get_subject_and_user(
        self, subject_id, user_id
    ) -> Union[Response, Tuple[Subject, User]]:
        if not subject_id or not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            subject = Subject.objects.get(id=subject_id)
            user = User.objects.get(id=user_id)
        except (Topic.DoesNotExist, User.DoesNotExist):
            raise Http404
        return subject, user

    def get_serializer_context(self) -> Dict[str, Union[None, Request, GenericAPIView]]:
        context = super().get_serializer_context()
        subject = self.kwargs["pk"]
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            raise Http404
        context["subject"] = subject
        return context

    def post(self, request, *args, **kwargs) -> Response:
        subject_id = self.kwargs["pk"]
        user_id = request.data
        subject, user = self.__get_subject_and_user(subject_id, user_id)
        subtopics_set = subject.subtopic_set.all()
        for topic in subtopics_set:
            topic.user.add(user)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        subject_id = self.kwargs["pk"]
        user_id = request.data
        subject, user = self.__get_subject_and_user(subject_id, user_id)
        subtopics_set = subject.subtopic_set.filter(user=user).all()
        for topic in subtopics_set:
            topic.user.remove(user)
        return Response(status=status.HTTP_200_OK)


class UserSearchBoxSubtopicView(generics.ListAPIView):
    serializer_class = UserSearchBoxSerializer
    permission_classes = [FileAccessPermission]

    class Access(enum.Enum):
        HAS_ACCESS = ("1",)
        NO_ACCESS = "0"

        @classmethod
        def from_str(cls, val):
            if val in "1":
                return cls.HAS_ACCESS
            elif val in "0":
                return cls.NO_ACCESS

    def __get_user_by_name_or_surname_access(
        self, text, topic, filter_by
    ) -> QuerySet[User]:
        if filter_by == "first_name":
            return (
                User.objects.filter(first_name__contains=text)
                .filter(groups__name="Student")
                .filter(topic=topic)
                .all()
            )

        elif filter_by == "last_name":
            return (
                User.objects.filter(last_name__contains=text)
                .filter(groups__name="Student")
                .filter(topic=topic)
                .all()
            )

    def with_access(self, text, topic) -> QuerySet[User]:
        filter = self.__get_user_by_name_or_surname_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.split(" ")
            first_text = space[0]
            second_text = space[1]
            queryset = (
                filter(text=first_text, topic=topic, filter_by="first_name")
                or filter(text=second_text, topic=topic, filter_by="first_name")
                or filter(text=first_text, topic=topic, filter_by="last_name")
                or filter(text=second_text, topic=topic, filter_by="last_name")
            )

        else:
            queryset = filter(text=text, topic=topic, filter_by="first_name") or filter(
                text=text, topic=topic, filter_by="last_name"
            )

        return queryset

    def __get__user_by_name_or_surname_no_access(
        self, text, topic, filter_by
    ) -> QuerySet[User]:
        if filter_by == "first_name":
            return (
                User.objects.exclude(topic=topic)
                .filter(first_name__contains=text)
                .filter(groups__name="Student")
                .all()
            )

        elif filter_by == "last_name":
            return (
                User.objects.exclude(topic=topic)
                .filter(last_name__contains=text)
                .filter(groups__name="Student")
                .all()
            )

    def no_access(self, text, topic) -> QuerySet[User]:
        filter = self.__get__user_by_name_or_surname_no_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.split(" ")
            first_text = space[0]
            second_text = space[1]
            queryset = (
                filter(text=first_text, topic=topic, filter_by="first_name")
                or filter(text=second_text, topic=topic, filter_by="first_name")
                or filter(text=first_text, topic=topic, filter_by="last_name")
                or filter(text=second_text, topic=topic, filter_by="last_name")
            )

        else:
            queryset = filter(text=text, topic=topic, filter_by="first_name") or filter(
                text=text, topic=topic, filter_by="last_name"
            )
        return queryset

    def get_queryset(self) -> QuerySet[User]:
        subtopic_id = self.kwargs["pk"]
        text = self.request.GET.get("text")
        access = self.request.GET.get("access")
        access = self.Access.from_str(access)

        try:
            topic = Topic.objects.get(id=subtopic_id)
        except Topic.DoesNotExist:
            raise Http404

        if access == self.Access.HAS_ACCESS:
            return self.with_access(text, topic)

        if access == self.Access.NO_ACCESS:
            return self.no_access(text, topic)

        raise ValidationError(detail="Access parameter can be 0 or 1")


class UserSearchBoxSubjectView(generics.ListAPIView):
    serializer_class = UserSearchBoxSerializer
    permission_classes = [FileAccessPermission]

    class Access(enum.Enum):
        HAS_ACCESS = ("1",)
        NO_ACCESS = "0"

        @classmethod
        def from_str(cls, val):
            if val in "1":
                return cls.HAS_ACCESS
            elif val in "0":
                return cls.NO_ACCESS

    def __get_user_by_name_or_surname_access(self, text, filter_by) -> QuerySet[User]:
        if filter_by == "first_name":
            return (
                User.objects.filter(first_name__contains=text)
                .filter(groups__name="Student")
                .all()
            )

        elif filter_by == "last_name":
            return (
                User.objects.filter(last_name__contains=text)
                .filter(groups__name="Student")
                .all()
            )

    def __iterate_queryset(self, queryset, subtopics, access) -> list:
        if not queryset:
            return queryset
        users_list = list(queryset)

        for user in queryset:
            for topic in subtopics:
                users_set = topic.user.all()
                if access:
                    if user not in users_set:
                        users_list.remove(user)
                        break
                else:
                    if user not in users_set:
                        break

        return users_list

    def __get_queryset_from_text(self, text, subject) -> Tuple[QuerySet[User], Topic]:
        subtopics = Topic.objects.filter(subject=subject).all()
        filter = self.__get_user_by_name_or_surname_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.split(" ")
            first_text = space[0]
            second_text = space[1]
            queryset = (
                filter(text=first_text, filter_by="first_name")
                or filter(text=second_text, filter_by="first_name")
                or filter(text=first_text, filter_by="last_name")
                or filter(text=second_text, filter_by="last_name")
            )

        else:
            queryset = filter(text=text, filter_by="first_name") or filter(
                text=text, filter_by="last_name"
            )

        return queryset, subtopics

    def with_access(self, text, subject):
        queryset, subtopics = self.__get_queryset_from_text(text, subject)
        return self.__iterate_queryset(queryset, subtopics, True)

    def no_access(self, text, subject):
        queryset, subtopics = self.__get_queryset_from_text(text, subject)
        return self.__iterate_queryset(queryset, subtopics, False)

    def get_queryset(self) -> list:
        subject_id = self.kwargs["pk"]
        text = self.request.GET.get("text")
        access = self.request.GET.get("access")
        access = self.Access.from_str(access)

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise Http404

        if access == self.Access.HAS_ACCESS:
            return self.with_access(text, subject)

        if access == self.Access.NO_ACCESS:
            return self.no_access(text, subject)

        raise ValidationError(detail="Access parameter can be 0 or 1")
