from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from django.apps import apps
from .models import TrnQuestPart, TrnQuest, Student, Question, Class
from django.db.models import QuerySet

import pandas as pd
import json

# Create your views here.



@api_view(['GET'])
def index(request):
  return Response('mt2610')


class UploadFileApiView(APIView):
  
  # permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    class_name = request.GET['squad_name']
    return Response(squad_name_check(class_name))

  def post(self, request, *args, **kwargs):
    data_return = process_upload_file(request)
    return Response(data_return)

def squad_name_check(class_name):
  return not Class.objects.filter(name=class_name)

def process_upload_file(request):
  file= request.FILES['file']
  class_name = request.POST['squad_name']

  if not file.name.endswith(('.xlsx','.xls')):
    raise ValidationError('Neeed Excel File!')
  else:
    data = pd.read_excel(file,sheet_name=0)
    no_question_cols = len([col for col in data.columns if 'Question ' in col])
    noofstudent = len(data.index)
    class_table = Class(name=class_name, noofstudent=noofstudent)
    error_code = 0
    error_line = set()
    try:
      with transaction.atomic():
          class_table.save()
          for row in range(data.shape[0]):
              studid = data.iat[row,3]
              name = str(data.iat[row,0]) + str(data.iat[row,1])
              index_temp = 12
              classid = Class.objects.filter(name=class_name).values('classid')
              student = Student(studid=studid, classid= classid, name=name)
              try:
                with transaction.atomic():
                  student.save()
              except IntegrityError:
                error_code = 1
                error_line.add(row+1)
                pass
              for i in range (0,no_question_cols):
                questionid = data.iat[row,index_temp]
                partid = data.iat[row,index_temp+1]
                response = data.iat[row,index_temp+3]
                if pd.isna(response):
                  response = ''
                index_temp +=5

                if pd.isna(partid):
                  trnquest = TrnQuest(studid=studid,questionid=questionid,response=response)
                  try:
                    with transaction.atomic():
                      trnquest.save()
                  except IntegrityError:
                    error_code = 1
                    error_line.add(row+1)
                    pass

                else:
                  trnquestpart = TrnQuestPart(studid=studid,questionid=questionid,partid=partid,partresponse=response)
                  try:
                    with transaction.atomic():
                      trnquestpart.save()
                  except IntegrityError:
                    error_code = 1
                    error_line.add(row+1)
                    pass
    except IntegrityError:
      transaction.rollback()
      pass
    else:
      transaction.commit()

  if len(error_line) !=0 or error_code == 1:
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"

  data_return = {"errorCode": error_code, "message": msg}
  return data_return