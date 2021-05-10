
from django.urls import path, include
from . import views

urlpatterns = [
  path('upload-xlsx', views.UploadFileApiView.as_view(), name="upload-file-api"),
]
