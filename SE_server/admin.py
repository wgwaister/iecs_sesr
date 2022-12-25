from django.contrib import admin
from .models import *
from guardian.admin import GuardedModelAdmin


class CompanyAdmin(GuardedModelAdmin):
    list_display = ('CompanyName', 'CompanyCode')


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('ProjectName', 'ProjectCode', 'CalculateStartDate', 'CalculateEndDate')
    ordering = ('ProjectCode',)


class MailListAdmin(GuardedModelAdmin):
    list_display = ('MailNumber', 'Type', 'Title', 'Sender', 'HasAtt')


class TestMemberListAdmin(GuardedModelAdmin):
    list_display = ('ProjectCode', 'MemberNumber', 'UnitName', 'Email')
    ordering = ('MemberNumber',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(MailList, MailListAdmin)
admin.site.register(TestMemberList, TestMemberListAdmin)
admin.site.register(Score)
admin.site.register(ReportBackRecord)
# Register your models here.
