from django.db import models

# Create your models here.

class Question(models.Model):
  class Meta: 
    db_table = "Question"

  question_id = models.BigIntegerField(db_column='QuestionID', primary_key=True)
  description = models.CharField(db_column='Description', max_length=256)
  model_ans = models.CharField(db_column='ModelAns', max_length=256)
  active_status = models.CharField(db_column='ActiveStatus', max_length=64)
  part_status = models.CharField(db_column='PartStatus', max_length=64)
  quest_total_mark = models.FloatField(db_column='QuestTotalMark')
  updated_by = models.CharField(db_column='UpdatedBy', max_length=256)
  archived_by = models.CharField(db_column='ArchivedBy', max_length=256)
  added_by = models.CharField(db_column='AddedBy', max_length=256)
  question = models.CharField(db_column='Question', max_length=256)

  def __str__(self):
    return '%d %s %s' % (question_id, question, model_ans)


class Trainee(models.Model):
  class Meta: 
    db_table = "Trainee"

  trainee_id = models.BigIntegerField(db_column='TraineeID', primary_key=True)
  name = models.CharField(db_column='Name', max_length=256)
  nric = models.CharField(db_column='NRIC', max_length=256)
  squad_id = models.CharField(db_column='SquadID', max_length=256)

  def __str__(self):
    return '%d %s %s' % (trainee_id, name)

class TrnQuest(models.Model):
  class Meta: 
    db_table = "TrnQuest"
    managed = True
    unique_together = (('trainee_id', 'question_id'),)

  trn_quest_id = models.BigIntegerField(db_column='TrnQuestID', primary_key=True)
  trainee_id = models.ForeignKey(Trainee, models.CASCADE, db_column='TraineeID')
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID')
  response = models.CharField(db_column='Response', max_length=256)
  trn_mark = models.FloatField(db_column='TrnMark')
  reason = models.CharField(db_column='Reason', max_length=256)
  other = models.CharField(db_column='Other', max_length=256)
  moderated_by = models.CharField(db_column='ModeratedBy', max_length=256)
  date_marked = models.DateField(db_column='DateMarked')
  date_moderated = models.DateField(db_column='DateModerated')

  def __str__(self):
    return '%d %s %s' % (trainee_id, question_id, response, trn_mark)


class QuestionPart(models.Model):
  class Meta: 
    db_table = "QuestionPart"
    managed = True
    unique_together = (('part_id', 'question_id'),)

  part_id = models.BigIntegerField(db_column='PartID', primary_key=True)
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID')
  part_desc = models.CharField(db_column='PartDesc', max_length=256)
  part_model_ans = models.CharField(db_column='PartModelAns', max_length=256)
  part_total_mark = models.FloatField(db_column='PartTotalMark')

  def __str__(self):
    return '%d %s %s' % (part_id, question_id, part_desc, part_total_mark)

class TrnQuestPart(models.Model):
  class Meta: 
    db_table = "TrnQuestPart"
    managed = True
    unique_together = (('trainee_id', 'question_id', 'part_id'),)

  trn_quest_part_id = models.BigIntegerField(db_column='TrnQuestPartID', primary_key=True)
  trainee_id = models.ForeignKey(Trainee, models.CASCADE, db_column='TraineeID')
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID')
  part_id = models.ForeignKey(QuestionPart, models.CASCADE, db_column='PartID')

  part_response = models.CharField(db_column='PartResponse', max_length=256)
  reason = models.CharField(db_column='Reason', max_length=256)
  other = models.CharField(db_column='Other', max_length=256)
  moderated_by = models.CharField(db_column='ModeratedBy', max_length=256)
  date_moderated = models.DateField(db_column='DateModerated')
  trn_part_mark = models.FloatField(db_column='TrnPartMark')
  

  def __str__(self):
    return '%d %s %s' % (trainee_id, question_id, part_id, part_response)