from django.contrib import admin

from .models import Exercise, ExerciseTest, Language


@admin.register(Exercise)
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register([Language, ExerciseTest])
