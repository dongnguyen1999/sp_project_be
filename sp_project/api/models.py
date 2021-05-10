from django.db import models

# Create your models here.
class Class(models.Model):
  class Meta:
    db_table = "Class"
  class_id = models.BigIntegerField(db_column='ClassID', primary_key=True)
  name = models.CharField(db_column='Name', max_length=256)
  no_of_student = models.IntegerField(db_column='NoOfStudent')

  def __str__(self):
    return '%d %s %d' % (class_id, name, no_of_student)

class Question(models.Model):
  class Meta: 
    db_table = "Question"
  question_id = models.BigIntegerField(db_column='QuestionID', primary_key=True)
  description = models.CharField(db_column='Description', max_length=256, blank=True)
  question = models.CharField(db_column='Question', max_length=256, null=True)
  model_ans = models.CharField(db_column='ModelAns', max_length=256)
  active_status = models.BooleanField(db_column='ActiveStatus', default=True)
  part_status = models.BooleanField(db_column='PartStatus', default=False)
  quest_total_mark = models.FloatField(db_column='QuestTotalMark', default=0)
  updated_by = models.CharField(db_column='UpdatedBy', max_length=256, null=True)
  archived_by = models.CharField(db_column='ArchivedBy', max_length=256, null=True)
  added_by = models.CharField(db_column='AddedBy', max_length=256, null=True)

  def __str__(self):
    return '%d %s %s' % (question_id, question, model_ans)


class Student(models.Model):
  class Meta: 
    db_table = "Student"

  student_id = models.BigIntegerField(db_column='StudID', primary_key=True)
  name = models.CharField(db_column='Name', max_length=256)
  nric = models.CharField(db_column='NRIC', max_length=256, null=True)
  class_id = models.ForeignKey(Class, models.CASCADE, db_column='ClassID')

  def __str__(self):
    return '%d %s' % (student_id, name)

class TrnQuest(models.Model):
  class Meta: 
    db_table = "TrnQuest"
    managed = True
    unique_together = (('student_id', 'question_id'),)

  trn_quest_id = models.BigIntegerField(db_column='TrnQuestID', primary_key=True)
  student_id = models.ForeignKey(Student, models.CASCADE, db_column='StudID', null=True)
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID', null=True)
  response = models.CharField(db_column='Response', max_length=256, null=True)
  trn_mark = models.FloatField(db_column='TrnMark', null=True)
  reason = models.CharField(db_column='Reason', max_length=256, null=True)
  other = models.CharField(db_column='Other', max_length=256, null=True)
  moderated_by = models.CharField(db_column='ModeratedBy', max_length=256, null=True)
  date_moderated = models.DateField(db_column='DateModerated', null=True)
  date_marked = models.DateField(db_column='DateMarked', auto_now=True)

  def __str__(self):
    return '%d %s %s %f' % (student_id, question_id, response, trn_mark)


class QuestionPart(models.Model):
  class Meta: 
    db_table = "QuestionPart"
    managed = True
    unique_together = (('part_id', 'question_id'),)

  question_part_id = models.AutoField(primary_key=True)
  part_id = models.CharField(db_column='PartID', max_length=5)
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID', null=True)
  part_question = models.CharField(db_column='PartQuestion', max_length=256, null=True)
  part_model_ans = models.CharField(db_column='PartModelAns', max_length=256)
  part_total_mark = models.FloatField(db_column='PartTotalMark', default=0)

  def __str__(self):
    return '%d %s %s %s' % (part_id, question_id, part_question, part_total_mark)

class TrnQuestPart(models.Model):
  class Meta: 
    db_table = "TrnQuestPart"
    managed = True
    unique_together = (('student_id', 'question_id', 'part_id'),)

  trn_quest_part_id = models.BigIntegerField(db_column='TrnQuestPartID', primary_key=True)
  student_id = models.ForeignKey(Student, models.CASCADE, db_column='StudID', null=True)
  question_id = models.ForeignKey(Question, models.CASCADE, db_column='QuestionID', null=True)
  part_id = models.ForeignKey(QuestionPart, models.CASCADE, db_column='PartID', null=True)

  part_response = models.CharField(db_column='PartResponse', max_length=256)
  trn_part_mark = models.FloatField(db_column='TrnPartMark', null=True)

  reason = models.CharField(db_column='Reason', max_length=256, null=True)
  other = models.CharField(db_column='Other', max_length=256, null=True)
  moderated_by = models.CharField(db_column='ModeratedBy', max_length=256, null=True)
  date_moderated = models.DateField(db_column='DateModerated', null=True)

  date_marked = models.DateField(db_column='DateMarked', auto_now=True)

  def __str__(self):
    return '%d %s %s' % (student_id, question_id, part_id, part_response)