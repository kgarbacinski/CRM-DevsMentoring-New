from django.urls import path
from Exercises_checker.api.views import (
    CreateTokenBaseView,
    ExerciseCodeView,
    ExerciseView,
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
<<<<<<< HEAD
    path("access/exercises/<int:pk>",
         ExerciseView.as_view(), name="exercise_access"),
    path("access/exercises/code/<int:pk>",
         ExerciseCodeView.as_view(), name="exercise_code"),
    path('token/', CreateTokenBaseView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
=======
    path("access/exercises/<int:pk>", ExerciseView.as_view(), name="exercise_access"),
    path(
        "access/exercises/code/<int:pk>",
        ExerciseCodeView.as_view(),
        name="exercise_code",
    ),
    path("token/", CreateTokenBaseView.as_view(), name="token_obtain_pair"),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
>>>>>>> feat/Add-pre-hooks
