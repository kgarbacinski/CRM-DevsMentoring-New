from django.contrib import admin
from .models import ProgrammingPath, Subject, Topic, Document


@admin.register(ProgrammingPath)
class ProgrammingPathAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

