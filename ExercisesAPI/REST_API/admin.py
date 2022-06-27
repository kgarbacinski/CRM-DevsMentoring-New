from django.contrib import admin

from .models import Exercise, ExerciseTest, Language

admin.site.register([Language, Exercise, ExerciseTest])
