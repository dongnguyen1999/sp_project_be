from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status

# Create your views here.

@api_view(['GET'])
def index(request):
  return Response('mt2610')


class UploadFileApiView(APIView):
  
  # permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    return Response('get')

  def post(self, request, *args, **kwargs):
    return Response('post')
