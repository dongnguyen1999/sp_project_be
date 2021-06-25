# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Class(models.Model):
    classid = models.AutoField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=256, db_column='Name', blank=True, null=True)  # Field name made lowercase.
    noofstudent = models.IntegerField(db_column='NoOfStudent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'


class Question(models.Model):
    questionid = models.AutoField(db_column='QuestionID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=256, db_column='Description', blank=True, null=True)  # Field name made lowercase.
    question = models.CharField(max_length=256, db_column='Question', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.SmallIntegerField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    partstatus = models.SmallIntegerField(db_column='PartStatus', blank=True, null=True)  # Field name made lowercase.
    questiontotalmark = models.TextField(db_column='QuestionTotalMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    archivedby = models.CharField(max_length=256, db_column='ArchivedBy', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(max_length=256, db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(max_length=256, db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Question'


class QuestionAns(models.Model):
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    ansid = models.IntegerField(db_column='AnsID')  # Field name made lowercase.
    modelans = models.CharField(max_length=256, db_column='ModelAns', blank=True, null=True)  # Field name made lowercase.
    ansmark = models.TextField(db_column='AnsMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'QuestionAns'
        unique_together = (('questionid', 'ansid'),)


class QuestionPart(models.Model):
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    partid = models.CharField(max_length=256, db_column='PartID')  # Field name made lowercase.
    partquestion = models.CharField(max_length=256, db_column='PartQuestion', blank=True, null=True)  # Field name made lowercase.
    parttotalmark = models.TextField(db_column='PartTotalMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'QuestionPart'
        unique_together = (('questionid', 'partid'),)


class QuestionPartAns(models.Model):
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    partid = models.CharField(max_length=256, db_column='PartID')  # Field name made lowercase.
    partansid = models.IntegerField(db_column='PartAnsID')  # Field name made lowercase.
    modelans = models.CharField(max_length=256, db_column='ModelAns', blank=True, null=True)  # Field name made lowercase.
    ansmark = models.TextField(db_column='AnsMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'QuestionPartAns'
        unique_together = (('questionid', 'partid', 'partansid'),)


class Student(models.Model):
    studid = models.AutoField(db_column='StudID', primary_key=True)  # Field name made lowercase.
    classid = models.IntegerField(db_column='ClassID')  # Field name made lowercase.
    name = models.CharField(max_length=256, db_column='Name', blank=True, null=True)  # Field name made lowercase.
    nric = models.TextField(db_column='NRIC', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Student'


class TrnQuest(models.Model):
    studid = models.IntegerField(db_column='StudID')  # Field name made lowercase.
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    response = models.CharField(max_length=256, db_column='Response', blank=True, null=True)  # Field name made lowercase.
    trnmark = models.CharField(max_length=256, db_column='TrnMark', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=256, db_column='Reason', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(max_length=256, db_column='Other', blank=True, null=True)  # Field name made lowercase.
    moderatedby = models.DateField(db_column='ModeratedBy', blank=True, null=True)  # Field name made lowercase.
    datemoderated = models.DateField(db_column='DateModerated', blank=True, null=True)  # Field name made lowercase.
    datemarked = models.DateField(db_column='DateMarked', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrnQuest'
        unique_together = (('studid', 'questionid'),)


class TrnQuestPart(models.Model):
    studid = models.IntegerField(db_column='StudID')  # Field name made lowercase.
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    partid = models.CharField(max_length=256, db_column='PartID')  # Field name made lowercase.
    partresponse = models.CharField(max_length=256, db_column='PartResponse', blank=True, null=True)  # Field name made lowercase.
    trnpartmark = models.CharField(max_length=256, db_column='TrnPartMark', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(max_length=256, db_column='Other', blank=True, null=True)  # Field name made lowercase.
    moderatedby = models.DateField(db_column='ModeratedBy', blank=True, null=True)  # Field name made lowercase.
    datemoderated = models.DateField(db_column='DateModerated', blank=True, null=True)  # Field name made lowercase.
    datemarked = models.DateField(db_column='DateMarked', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=256, db_column='Reason', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrnQuestPart'
        unique_together = (('studid', 'questionid', 'partid'),)
