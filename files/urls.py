from django.urls import path
from .views import FileListView, FileUploadView, FileDeleteView

urlpatterns = [
    path('', FileListView.as_view(), name='file_list'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
]