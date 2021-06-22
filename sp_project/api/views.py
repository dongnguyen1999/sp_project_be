import os
from collections import defaultdict,OrderedDict
from django.apps import apps
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
  def delete(self, request, *args, **kwargs):
    data=json.loads(request.body)
    if data["type"] == 0:
      data_return=cancel(data["hash"])
    elif data["type"] == 1:
      data_return=clear_log(data["hash"])
    else:
      error_code = 1
      msg = "Invalid type!"
      data_return = {"errorCode": error_code, "message": msg}
    return Response(data_return)

  def get(self, request, *args, **kwargs):
    class_name = request.GET['squad_name']
    return Response(squad_name_check(class_name))

  def post(self, request, *args, **kwargs):
    file_type = request.POST['file_type']
    if file_type == 'response-set':
      data_return = process_response_set(request)
    if file_type == 'marking-scheme':
      data_return = process_marking_scheme(request)
    if file_type =='cancel':
      cancel(request)
      data_return = "Done"
    return Response(data_return)

def squad_name_check(class_name):
  return not Class.objects.filter(name=class_name)


def process_response_set(request):
  file= request.FILES['file']
  class_name = request.POST['squad_name']
  hash = request.POST['hash']
  dict_json = defaultdict(list)
  if not file.name.endswith(('.xlsx','.xls')):
    raise ValidationError('Neeed Excel File!')
  else:
    data = pd.read_excel(file,sheet_name=0)
    no_question_cols = len([col for col in data.columns if 'Question ' in col])
    noofstudent = len(data.index)
    class_table = Class(name=class_name, noofstudent=noofstudent)
    error_code = 0
    error_line = set()
    error_studid = set()
    for row in range(data.shape[0]):
      studid = data.iat[row, 3]
      if Student.objects.filter(studid=studid).values('studid'):
        error_studid.add(studid)
        error_code = -1
    if error_code != -1:
      try:
        with transaction.atomic():
            class_table.save()
            classid = Class.objects.filter(name=class_name).values('classid')
            dict_json['Class'].append({'classid':classid[0]['classid']})
            dict_json.update()
      except IntegrityError:
            transaction.rollback()
            pass
      else:
        transaction.commit()
        for row in range(data.shape[0]):
            studid = data.iat[row,3]
            name = str(data.iat[row,0]) + str(data.iat[row,1])
            index_temp = 12
            student = Student(studid=studid, classid= classid, name=name)
            try:
              with transaction.atomic():
                student.save()
                dict_json['Student'].append({'studid': int(studid)})
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
                    dict_json['TrnQuest'].append({'studid':int(studid), 'questionid':int(questionid)})
                except IntegrityError:
                  error_code = 1
                  error_line.add(row+1)
                  transaction.rollback()
                  pass
                else:
                  transaction.commit()
              else:
                trnquestpart = TrnQuestPart(studid=studid,questionid=questionid,partid=partid,partresponse=response)
                try:
                  with transaction.atomic():
                    trnquestpart.save()
                    dict_json['TrnQuestPart'].append({'studid':int(studid), 'questionid':int(questionid), 'partid':partid})
                except IntegrityError:
                  error_code = 1
                  error_line.add(row+1)
                  transaction.rollback()
                  pass
                else:
                  transaction.commit()

  if error_code == -1:
    msg = "Student are already in database: " + str(error_studid)
  elif len(error_line) !=0 or error_code == 1:
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"
    with open(hash+".json","w") as file:
      json.dump(dict_json,file)
  data_return = {"errorCode": error_code, "message": msg}
  return data_return

def process_marking_scheme(request):
  file= request.FILES['file']
  hash = request.POST['hash']
  dict_json = defaultdict(list)
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
        ansid_temp = QuestionAns.objects.aggregate(Max('ansid'))['ansid__max'] +1
      modelans = data_filtered.iat[row,3]
      ansmark = data_filtered.iat[row,4]
      questionans = QuestionAns(questionid=questionid,ansid=ansid_temp,modelans=modelans,ansmark=ansmark)
      try:
        with transaction.atomic():
          questionans.save()
          dict_json['QuestionAns'].append({'questionid':int(questionid), 'ansid': ansid_temp})
      except IntegrityError:
        error_code = 1
        error_line.add(row+1)
        transaction.rollback()
        pass
      else:
        transaction.commit()

    data_filtered=data[~data.isin(data_filtered)]
    data_filtered= data_filtered.dropna(subset=['questionID'])
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
      modelans = data_filtered.iat[row, 3]
      ansmark = data_filtered.iat[row, 4]
      questionpartans = QuestionPartAns(questionid=questionid, partid=partid ,partansid=ansid_temp, modelans=modelans, ansmark=ansmark)
      try:
        with transaction.atomic():
          questionpartans.save()
          dict_json['QuestionPartAns'].append({'questionid': int(questionid), 'partid': partid, 'partansid':ansid_temp})
      except IntegrityError:
        error_code = 1
        error_line.add(row + 1)
        transaction.rollback()
        pass
      else:
        transaction.commit()
  if len(error_line) !=0 or error_code == 1:
    msg = "Insert fail at row(s): " + str(error_line)
  else:
    msg = "Insert successful"
    with open(hash+".json","w") as file:
      json.dump(dict_json,file)
  data_return = {"errorCode": error_code, "message": msg}
  return data_return

def clear_log(hash):
  file = hash + ".json"
  if os.path.exists(file):
    os.remove(file)
    error_code = 0
    msg = "Done"
  else:
    error_code = 1
    msg = "The log file does not exist"
  data_return = {"errorCode": error_code, "message": msg}
  return data_return



def cancel(hash):
  file = hash + ".json"
  with open(file) as datafile:
    data = json.load(datafile)
    data = OrderedDict(sorted(data.items(),reverse=True))
    print(data)
  for key in data.keys():
    for i in range(0,len(data[key])):
      model = apps.get_model('api',key)
      model.objects.filter(**data[key][i]).delete()
  data_return = clear_log(hash)
  return data_return