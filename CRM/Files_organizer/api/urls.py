from django.urls import path

from .views import DocumentView, HasAccessToFileView, HasAccessToSubjectView, UserSearchBoxSubtopicView, \
    UserSearchBoxSubjectView

urlpatterns = [
    path('files/<int:pk>/', DocumentView.as_view(), name='documents'),
    path('access/files/<int:pk>/', HasAccessToFileView.as_view(), name='file_access'),
    path('access/subject/<int:pk>/', HasAccessToSubjectView.as_view(), name='subject_access'),
    path('access/searchbox/subtopic/<int:pk>/', UserSearchBoxSubtopicView.as_view(), name='subtopic_searchbox'),
    path('access/searchbox/subject/<int:pk>/', UserSearchBoxSubjectView.as_view(), name='subject_searchbox'),
]
