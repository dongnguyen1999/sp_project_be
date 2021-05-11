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
    name = models.CharField(max_length=255, db_column='Name', blank=True, null=True)  # Field name made lowercase.
    noofstudent = models.IntegerField(db_column='NoOfStudent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'


class Question(models.Model):
    questionid = models.AutoField(db_column='QuestionID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, db_column='Description', blank=True, null=True)  # Field name made lowercase.
    modelans = models.CharField(max_length=255, db_column='ModelAns', blank=True, null=True)  # Field name made lowercase.
    question = models.CharField(max_length=255, db_column='Question', blank=True, null=True)  # Field name made lowercase.
    activestatus = models.SmallIntegerField(db_column='ActiveStatus', blank=True, null=True)  # Field name made lowercase.
    partstatus = models.SmallIntegerField(db_column='PartStatus', blank=True, null=True)  # Field name made lowercase.
    questtotalmark = models.TextField(db_column='QuestTotalMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    archivedby = models.CharField(max_length=255, db_column='ArchivedBy', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(max_length=255, db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    addedby = models.CharField(max_length=255, db_column='AddedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Question'


class QuestionPart(models.Model):
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    partid = models.CharField(max_length=255, db_column='PartID')  # Field name made lowercase.
    partquestion = models.CharField(max_length=255, db_column='PartQuestion', blank=True, null=True)  # Field name made lowercase.
    partmodelans = models.CharField(max_length=255, db_column='PartModelAns', blank=True, null=True)  # Field name made lowercase.
    parttotalmark = models.TextField(db_column='PartTotalMark', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'QuestionPart'
        unique_together = (('questionid', 'partid'),)


class Student(models.Model):
    studid = models.AutoField(db_column='StudID', primary_key=True)  # Field name made lowercase.
    classid = models.IntegerField(db_column='ClassID')  # Field name made lowercase.
    name = models.CharField(max_length=255, db_column='Name', blank=True, null=True)  # Field name made lowercase.
    nric = models.TextField(db_column='NRIC', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Student'


class TrnQuest(models.Model):
    studid = models.IntegerField(db_column='StudID')  # Field name made lowercase.
    questionid = models.IntegerField(db_column='QuestionID')  # Field name made lowercase.
    response = models.CharField(max_length=255, db_column='Response', blank=True, null=True)  # Field name made lowercase.
    trnmark = models.CharField(max_length=255, db_column='TrnMark', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=255, db_column='Reason', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(max_length=255, db_column='Other', blank=True, null=True)  # Field name made lowercase.
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
    partid = models.CharField(max_length=255, db_column='PartID')  # Field name made lowercase.
    partresponse = models.CharField(max_length=255, db_column='PARTRESPONSE', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(max_length=255, db_column='Other', blank=True, null=True)  # Field name made lowercase.
    moderatedby = models.DateField(db_column='ModeratedBy', blank=True, null=True)  # Field name made lowercase.
    datemoderated = models.DateField(db_column='DateModerated', blank=True, null=True)  # Field name made lowercase.
    datemarked = models.DateField(db_column='DateMarked', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(max_length=255, db_column='Reason', blank=True, null=True)  # Field name made lowercase.

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
