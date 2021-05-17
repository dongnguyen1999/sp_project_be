from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from django.apps import apps
from  .models import TrnQuestPart, TrnQuest, Student, Question

import pandas as pd
import json

# Create your views here.

@api_view(['GET'])
def index(request):
  return Response('mt2610')


class UploadFileApiView(APIView):
  
  # permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    return Response('get')

  def post(self, request, *args, **kwargs):
    data_return=process_upload_file(request)
    return Response(data_return)

def process_upload_file(request):
  file= request.FILES['file']
  class_name = request.POST['squad_name']

  if not file.name.endswith(('.xlsx','.xls')):
    raise ValidationError('Neeed Excel File!')
  else:
    data = pd.read_excel(file,sheet_name=0)
    no_question_cols = len([col for col in data.columns if 'Question ' in col])
    for row in range(data.shape[0]):
        no_question_cols
        studid = data.iat[row,3]
        studid = Student.objects.get(studid=studid)
        index_temp = 12
        error_line =[]
        for i in range (0,no_question_cols):
          questionid = data.iat[row,index_temp]
          partid = data.iat[row,index_temp+1]
          response = data.iat[row,index_temp+3]
          if pd.isna(response):
            response = ''
          index_temp +=5

          if pd.isna(partid):
            questionid = Question.objects.get(questionid=questionid)
            trnquest = TrnQuest(studid=studid,questionid=questionid,response=response)
            try:
              trnquest.save()
              error_code = 0
            except IntegrityError as error:
              error_code = 1
              error_line.append(i+1)

          else:
            trnquestpart = TrnQuestPart(studid=studid,questionid=questionid,partid=partid,partresponse=response)
            try:
              trnquestpart.save()
              error_code = 0
            except IntegrityError:
              error_code = 1
              error_line.append(i+1)

  if len(error_line) !=0 :
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"

  data_return = {"errorCode": error_code, "message": msg}
  return data_return