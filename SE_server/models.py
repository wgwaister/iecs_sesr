from django.db import models
from django.contrib.auth.models import *
from django.core.files.storage import *


class Company(models.Model):
    GroupCode = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='Company')
    CompanyCode = models.CharField(max_length=255, primary_key=True)
    CompanyName = models.CharField(max_length=255)
    ProjectCount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.CompanyCode

    class Meta:
        permissions = (
            ('exe_company', 'Execute Company'),
        )


def html_upload_to(instance, filename):
    return 'MailFile/{project_code}/{filename}'.format(project_code=instance.ProjectCode, filename=filename)


class MailList(models.Model):
    ProjectCode = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='Mail')
    id = models.BigAutoField(primary_key=True)
    MailNumber = models.CharField(max_length=255)
    Type = models.CharField(max_length=100, null=True, blank=True)
    Title = models.CharField(max_length=255, null=True, blank=True)
    Sender = models.CharField(max_length=255, null=True, blank=True)
    Sender_Mail = models.CharField(max_length=255, null=True, blank=True)
    HasAtt = models.BooleanField(default=False, null=True, blank=True)
    Address = models.CharField(max_length=255)
    Open = models.CharField(max_length=255)
    Click = models.CharField(max_length=255)
    Attachment = models.CharField(max_length=255, null=True, blank=True)
    MailTag = models.CharField(max_length=255, null=True, blank=True, default=None)
    filepath = models.FileField(upload_to=html_upload_to, default=None, null=True, blank=True)
    AttachmentFile = models.FileField(upload_to=html_upload_to, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('ProjectCode', 'MailNumber')


class Project(models.Model):
    CompanyCode = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='Company', blank=True)
    ProjectCode = models.CharField(max_length=50, primary_key=True)
    ProjectName = models.CharField(max_length=255, blank=True)
    CalculateStartDate = models.DateTimeField(null=True, blank=True)
    CalculateEndDate = models.DateTimeField(null=True, blank=True)
    PersonCount = models.IntegerField(null=True, blank=True)
    UnitList = models.JSONField(null=True, blank=True)
    MailCount = models.IntegerField(null=True, blank=True)
    ProjectResult = models.JSONField(null=True, blank=True)
    OpenRecord = models.JSONField(null=True, blank=True, default=None)
    ClickRecord = models.JSONField(null=True, blank=True, default=None)
    AttachmentRecord = models.JSONField(null=True, blank=True, default=None)
    SendRecord = models.JSONField(null=True, blank=True, default=None)
    lastCalTime = models.DateTimeField(null=True, blank=True, default=None)
    IgnoreSecond = models.IntegerField(null=True, default=60)

    def __str__(self):
        return self.ProjectCode

    class Meta:
        permissions = (
            ('exe_project', 'Execute Project'),
        )


class TestMemberList(models.Model):
    ProjectCode = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='TestML')
    id = models.BigAutoField(primary_key=True)
    Unit = models.CharField(max_length=10, null=True, blank=True, )
    UnitName = models.CharField(max_length=255, null=True, blank=True, default=None)
    MemberNumber = models.CharField(max_length=10)
    UUID = models.CharField(max_length=20, null=True, blank=True)
    Email = models.EmailField()
    Result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.MemberNumber

    class Meta:
        unique_together = [('ProjectCode', 'MemberNumber'), ('ProjectCode', 'Email')]


class TestMemberListTemp(models.Model):
    ProjectCode = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='TestML_Temp')
    id = models.BigAutoField(primary_key=True)
    UnitName = models.CharField(max_length=255, null=True, blank=True, default=None)
    MemberNumber = models.CharField(max_length=10)
    UUID = models.CharField(max_length=20, null=True, blank=True)
    Email = models.EmailField()

    def __str__(self):
        return self.MemberNumber


class Log(models.Model):
    date = models.CharField(max_length=20, db_collation='utf8_general_ci')
    time = models.CharField(max_length=20, db_collation='utf8_general_ci')
    html = models.CharField(max_length=255, db_collation='utf8_general_ci')
    uuid = models.CharField(max_length=20, db_collation='utf8_general_ci')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'log'


class File(models.Model):
    ProjectCode = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='Mail_File', default=None)
    id = models.BigAutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    sender = models.CharField(max_length=255, default=None)
    filepath = models.FileField(upload_to=html_upload_to)


class Score(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='std_score', default=None)
    group_code = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    mail1 = models.IntegerField(null=True, blank=True)
    mail2 = models.IntegerField(null=True, blank=True)
    mail3 = models.IntegerField(null=True, blank=True)


class ReportBackRecord(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='std_rb', default=None)
    group_code = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    content = models.CharField(max_length=255, null=True, blank=True)
    check_result = models.BooleanField(null=True, blank=True)
    report_ime = models.DateTimeField(default=timezone.now)
# Create your models here.
