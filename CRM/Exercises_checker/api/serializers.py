from Exercises_checker.models import ExerciseStatus
from rest_framework import serializers


class PathExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseStatus
        fields = ["done"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = instance.exercise.id
        representation["name"] = instance.exercise.name
        representation["slug"] = instance.exercise.slug
        return representation


class ChangeExerciseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseStatus
<<<<<<< HEAD
        fields = ["code", "done"]
=======
        fields = ["code"]
>>>>>>> feat/Add-pre-hooks
