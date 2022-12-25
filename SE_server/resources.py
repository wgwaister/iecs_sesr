from .models import *
from import_export import resources


class TestMemberResources(resources.ModelResource):

    def __init__(self, *args, **kwargs):
        self._ProjectCode = kwargs.pop('ProjectCode', None)
        super().__init__(*args, **kwargs)

    def before_save_instance(self, instance, using_transactions, dry_run):
        setattr(instance, "ProjectCode", self._ProjectCode)

    def skip_row(self, instance, original):
        if instance.Email == 'test@example.tst' and instance.MemberNumber == 'M001' and instance.UnitName == '業務部':
            return True
        return False

    class Meta:
        model = TestMemberListTemp
        fields = ('MemberNumber', 'UnitName', 'Email', 'id')


class TestMemberUIDResources(resources.ModelResource):

    def __init__(self, *args, **kwargs):
        self._ProjectCode = kwargs.pop('ProjectCode', None)
        super().__init__(*args, **kwargs)

    def before_save_instance(self, instance, using_transactions, dry_run):
        setattr(instance, "ProjectCode", self._ProjectCode)

    def skip_row(self, instance, original):
        if instance.Email == 'test@example.tst' and instance.MemberNumber == 'M001' and instance.UnitName == '業務部' \
                and instance.UUID == 'EXA01M001EX':
            return True
        return False

    class Meta:
        model = TestMemberListTemp
        fields = ('MemberNumber', 'UnitName', 'UUID', 'Email', 'id')


class ProjectMailResources(resources.ModelResource):

    def __init__(self, *args, **kwargs):
        self._ProjectCode = kwargs.pop('ProjectCode', None)
        super().__init__(*args, **kwargs)

    def before_save_instance(self, instance, using_transactions, dry_run):
        setattr(instance, "ProjectCode", self._ProjectCode)

    def skip_row(self, instance, original):
        if instance.Address == '/example01/' or instance.Address == '/example02/':
            return True
        return False

    class Meta:
        model = MailList
        fields = ('MailNumber', 'HasAtt', 'Address', 'Open', 'Click', 'Attachment', 'id')
