from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from django.apps import apps
from .models import TrnQuestPart, TrnQuest, Student, QuestionAns,QuestionPartAns, Class
from django.db.models import QuerySet, Max

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
  @transaction.atomic()
  def post(self, request, *args, **kwargs):
    # file_type = request.POST['file_type']
    # if file_type == 'response-set':
    #   data_return = process_response_set(request)
    # if file_type == 'marking-scheme':
    #   data_return = process_marking_scheme(request)

    file = request.FILES['file']
    class_name = request.POST['squad_name']

    if not file.name.endswith(('.xlsx', '.xls')):
      raise ValidationError('Neeed Excel File!')
    else:
      data = pd.read_excel(file, sheet_name=0)
      no_question_cols = len([col for col in data.columns if 'Question ' in col])
      noofstudent = len(data.index)
      class_table = Class(name=class_name, noofstudent=noofstudent)
      error_code = 0
      error_line = set()
      try:
        class_table.save()
      except IntegrityError:
        transaction.rollback()
      for row in range(data.shape[0]):
        studid = data.iat[row, 3]
        name = str(data.iat[row, 0]) + str(data.iat[row, 1])
        index_temp = 12
        classid = Class.objects.filter(name=class_name).values('classid')
        student = Student(studid=studid, classid=classid, name=name)
        try:
          student.save()
        except IntegrityError:
          error_code = 1
          error_line.add(row + 1)
          transaction.rollback()
          break
        for i in range(0, no_question_cols):
          questionid = data.iat[row, index_temp]
          partid = data.iat[row, index_temp + 1]
          response = data.iat[row, index_temp + 3]
          if pd.isna(response):
            response = ''
          index_temp += 5
          if pd.isna(partid):
            trnquest = TrnQuest(studid=studid, questionid=questionid, response=response)
            try:
              trnquest.save()
            except IntegrityError:
              error_code = 1
              error_line.add(row + 1)
              transaction.rollback()
              break
          else:
            trnquestpart = TrnQuestPart(studid=studid, questionid=questionid, partid=partid, partresponse=response)
            try:
              trnquestpart.save()
            except IntegrityError:
              error_code = 1
              error_line.add(row + 1)
              transaction.rollback()
              break
    if len(error_line) != 0 or error_code == 1:
      msg = "Insert fail at row(s): " + str(error_line)
    else:
      msg = "Insert successful"

    data_return = {"errorCode": error_code, "message": msg}
    return Response(data_return)



def squad_name_check(class_name):
  return not Class.objects.filter(name=class_name)

@transaction.atomic()
def process_response_set(request):
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
      class_table.save()
    except IntegrityError:
      transaction.rollback()
      pass
    for row in range(data.shape[0]):
      studid = data.iat[row, 3]
      name = str(data.iat[row, 0]) + str(data.iat[row, 1])
      index_temp = 12
      classid = Class.objects.filter(name=class_name).values('classid')
      student = Student(studid=studid, classid=classid, name=name)
      try:
        student.save()
      except IntegrityError:
        error_code = 1
        error_line.add(row + 1)
        transaction.rollback()
        pass
      for i in range(0, no_question_cols):
        questionid = data.iat[row, index_temp]
        partid = data.iat[row, index_temp + 1]
        response = data.iat[row, index_temp + 3]
        if pd.isna(response):
          response = ''
        index_temp += 5
        if pd.isna(partid):
          trnquest = TrnQuest(studid=studid, questionid=questionid, response=response)
          try:
            trnquest.save()
          except IntegrityError:
            error_code = 1
            error_line.add(row + 1)
            transaction.rollback()
            pass
        else:
          trnquestpart = TrnQuestPart(studid=studid, questionid=questionid, partid=partid, partresponse=response)
          try:
            trnquestpart.save()
          except IntegrityError:
            error_code = 1
            error_line.add(row + 1)
            transaction.rollback()
            pass
  if len(error_line) !=0 or error_code == 1:
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"

  data_return = {"errorCode": error_code, "message": msg}
  return data_return

def process_marking_scheme(request):
  file= request.FILES['file']

  if not file.name.endswith(('.xlsx','.xls')):
    raise ValidationError('Neeed Excel File!')
  else:
    data = pd.read_excel(file,sheet_name=0)
    data_filtered = data[data['PartID'].isnull()]
    error_code = 0
    error_line = set()
    for row in range(data_filtered.shape[0]):
      questionid = data_filtered.iat[row,0]
      try:
        ansid_temp = QuestionAns.objects.filter(questionid=questionid).count()
      except IntegrityError:
        ansid_temp = 1
        pass
      if ansid_temp >1:
        ansid_temp = QuestionAns.objects.aggregate(Max('ansid')) +1
      modelans = data_filtered.iat[row,3]
      ansmark = data_filtered.iat[row,4]
      questionans = QuestionAns(questionid=questionid,ansid=ansid_temp,modelans=modelans,ansmark=ansmark)
      try:
        questionans.save()
      except IntegrityError:
        error_code = 1
        error_line.add(row+1)
        transaction.rollback()
        pass

    data_filtered=data[~data.isin(data_filtered)]
    for row in range(data_filtered.shape[0]):
      questionid = data_filtered.iat[row, 0]
      partid = data_filtered.iat[row, 1]
      try:
        ansid_temp = QuestionPartAns.objects.filter(questionid=questionid,partid=partid).count()
      except IntegrityError:
        ansid_temp = 1
        pass
      if ansid_temp > 1:
        ansid_temp = QuestionPartAns.objects.aggregate(Max('partansid'))['partansid__max'] +1
        print(ansid_temp)
      modelans = data_filtered.iat[row, 3]
      ansmark = data_filtered.iat[row, 4]
      questionpartans = QuestionPartAns(questionid=questionid, partid=partid ,partansid=ansid_temp, modelans=modelans, ansmark=ansmark)
      try:
        questionpartans.save()
      except IntegrityError:
        error_code = 1
        error_line.add(row + 1)
        transaction.rollback()
        pass
  if len(error_line) !=0 or error_code == 1:
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"

  data_return = {"errorCode": error_code, "message": msg}
  return data_return