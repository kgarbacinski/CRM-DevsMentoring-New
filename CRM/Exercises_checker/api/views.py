from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Exercises_checker.api.permissions import ExerciseCodePermission
from Exercises_checker.api.serializers import PathExerciseSerializer, ChangeExerciseCodeSerializer
from Exercises_checker.models import Language, Exercise, ExerciseStatus


class ExerciseView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PathExerciseSerializer

    def get_language_and_user(self):
        language_id = self.kwargs['pk']
        language = get_object_or_404(Language, id=language_id)
        user = self.request.user
        return language, user

    def get_all_exercises_quantity(self):
        language, user = self.get_language_and_user()
        all_exercises_quantity = Exercise.objects.filter(
            language__user=user).filter(language=language).count()
        done_exercises_quantity = ExerciseStatus.objects.filter(exercise__language=language).filter(user=user).filter(
            done=True).count()

        return all_exercises_quantity, done_exercises_quantity

    def get_queryset_exercise_list(self, type):
        language, user = self.get_language_and_user()
        queryset = ExerciseStatus.objects.filter(exercise__language=language)\
            .filter(exercise__type=type)\
            .filter(user=user).all()
        exercise_quantity = Exercise.objects.filter(language=language).filter(type=type).filter(
            language__user=user).count()
        done_exercise_quantity = queryset.filter(done=True).count()
        print(queryset)
        return queryset, exercise_quantity, done_exercise_quantity

    def list(self, request, *args, **kwargs):
        all_exercises_quantity, done_exercises_quantity = self.get_all_exercises_quantity()
        easy_exercises, easy_exercises_quantity, done_easy_exercises_quantity = self.get_queryset_exercise_list(
            type="EASY")
        medium_exercises, medium_exercises_quantity, done_medium_exercises_quantity = self.get_queryset_exercise_list(
            type="MEDIUM")
        hard_exercises, hard_exercises_quantity, done_hard_exercises_quantity = self.get_queryset_exercise_list(
            type="HARD")

        return Response({
            "quantity": {
                "all_exercises_quantity": all_exercises_quantity,
                "done_exercises_quantity": done_exercises_quantity,
                "easy_exercises_quantity": easy_exercises_quantity,
                "done_easy_exercises_quantity": done_easy_exercises_quantity,
                "medium_exercises_quantity": medium_exercises_quantity,
                "done_medium_exercises_quantity": done_medium_exercises_quantity,
                "hard_exercises_quantity": hard_exercises_quantity,
                "done_hard_exercises_quantity": done_hard_exercises_quantity,
            },
            "exercises": {
                "easy": self.serializer_class(easy_exercises, many=True).data,
                "medium": self.serializer_class(medium_exercises, many=True).data,
                "hard": self.serializer_class(hard_exercises, many=True).data,
            }
        })


class CreateTokenBaseView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def get(self, request, *args, **kwargs):
        user = AnonymousUser
        refresh = self.get_token(user)
        data = {"access": str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class ExerciseCodeView(APIView):
    permission_classes = [ExerciseCodePermission]
    serializer_class = ChangeExerciseCodeSerializer

    def patch(self, request, pk):
        exercise_status = ExerciseStatus.objects.filter(id=pk).first()
        print('DUPA - ', request.data.get('done'))
        # TODO JEŻELI JUZ ZROBIONE NIE AKTUALIZUJ
        if not exercise_status:
            raise Http404
        data = {"code": request.data.get('code'), "done": request.data.get('done')}
        # done = {"done": request.data.get('done')}
        serializer = self.serializer_class(
            exercise_status, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
