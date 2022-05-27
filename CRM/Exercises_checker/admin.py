from django.contrib import admin
from .models import Language, Exercise, ExerciseStatus, Hint


# Register your models here.
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ExerciseStatus)
class ExerciseStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    pass
