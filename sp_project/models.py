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
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    noofstudent = models.IntegerField(db_column='NoOfStudent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'


class Question(models.Model):
    questionid = models.AutoField(db_column='QuestionID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=256)  # Field name made lowercase.
    modelans = models.CharField(db_column='ModelAns', max_length=256)  # Field name made lowercase.
    activestatus = models.BooleanField(db_column='ActiveStatus')  # Field name made lowercase.
    partstatus = models.BooleanField(db_column='PartStatus')  # Field name made lowercase.
    questtotalmark = models.FloatField(db_column='QuestTotalMark')  # Field name made lowercase.
    archivedby = models.CharField(db_column='ArchivedBy', max_length=256, blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(db_column='AddedBy', max_length=256, blank=True, null=True)  # Field name made lowercase.
    question = models.CharField(db_column='Question', max_length=256, blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Question'


class Questionpart(models.Model):
    partid = models.CharField(db_column='PartID', primary_key=True, max_length=5)  # Field name made lowercase.
    partmodelans = models.CharField(db_column='PartModelAns', max_length=256)  # Field name made lowercase.
    parttotalmark = models.FloatField(db_column='PartTotalMark')  # Field name made lowercase.
    partquestion = models.CharField(db_column='PartQuestion', max_length=256, blank=True, null=True)  # Field name made lowercase.
    questionid = models.ForeignKey(Question, models.DO_NOTHING, db_column='QuestionID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QuestionPart'
        unique_together = (('partid', 'questionid'),)


class Student(models.Model):
    studid = models.AutoField(db_column='StudID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    nric = models.CharField(db_column='NRIC', max_length=256, blank=True, null=True)  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='ClassID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student'


class Trnquest(models.Model):
    trnquestid = models.AutoField(db_column='TrnQuestID', primary_key=True)  # Field name made lowercase.
    response = models.CharField(db_column='Response', max_length=256, blank=True, null=True)  # Field name made lowercase.
    trnmark = models.FloatField(db_column='TrnMark', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=256, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=256, blank=True, null=True)  # Field name made lowercase.
    moderatedby = models.CharField(db_column='ModeratedBy', max_length=256, blank=True, null=True)  # Field name made lowercase.
    datemarked = models.DateField(db_column='DateMarked')  # Field name made lowercase.
    datemoderated = models.DateField(db_column='DateModerated', blank=True, null=True)  # Field name made lowercase.
    questionid = models.ForeignKey(Question, models.DO_NOTHING, db_column='QuestionID', blank=True, null=True)  # Field name made lowercase.
    studid = models.ForeignKey(Student, models.DO_NOTHING, db_column='StudID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrnQuest'
        unique_together = (('studid', 'questionid'),)


class Trnquestpart(models.Model):
    trnquestpartid = models.AutoField(db_column='TrnQuestPartID', primary_key=True)  # Field name made lowercase.
    partresponse = models.CharField(db_column='PartResponse', max_length=256)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=256, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=256, blank=True, null=True)  # Field name made lowercase.
    moderatedby = models.CharField(db_column='ModeratedBy', max_length=256, blank=True, null=True)  # Field name made lowercase.
    datemoderated = models.DateField(db_column='DateModerated', blank=True, null=True)  # Field name made lowercase.
    trnpartmark = models.FloatField(db_column='TrnPartMark', blank=True, null=True)  # Field name made lowercase.
    partid = models.ForeignKey(Questionpart, models.DO_NOTHING, db_column='PartID', blank=True, null=True)  # Field name made lowercase.
    questionid = models.ForeignKey(Question, models.DO_NOTHING, db_column='QuestionID', blank=True, null=True)  # Field name made lowercase.
    datemarked = models.DateField(db_column='DateMarked')  # Field name made lowercase.
    studid = models.ForeignKey(Student, models.DO_NOTHING, db_column='StudID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrnQuestPart'
        unique_together = (('studid', 'questionid', 'partid'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
