from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="使用者名稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProjectSearch(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('CompanyCode', 'ProjectName')


class CompanySearch(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('CompanyCode',)


class ProjectForm(forms.ModelForm):
    CalculateStartDate = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Select a date',
                                          'type': 'datetime-local'})
    )
    CalculateEndDate = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Select a date',
                                          'type': 'datetime-local'})
    )

    class Meta:
        model = Project
        fields = ('CompanyCode', 'ProjectCode', 'ProjectName', 'CalculateStartDate', 'CalculateEndDate', 'IgnoreSecond')


class TestMemberForm(forms.ModelForm):
    class Meta:
        model = TestMemberList
        fields = ('ProjectCode', 'UnitName', 'MemberNumber', 'Email')


class ProjectMailForm(forms.ModelForm):
    class Meta:
        model = MailList
        fields = (
           'Title', 'Sender', 'Sender_Mail')


class UploadForm(forms.Form):
    upload = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'text/csv'})
    )


class HTMLUploadForm(forms.Form):
    upload = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'text/html'})
    )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('CompanyCode', 'CompanyName')
