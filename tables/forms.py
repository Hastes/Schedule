__author__ = 'Rom54'
from django import forms
from .models import Schedule

# class ParserForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         fields = ('schedule_file')
#     def clean_schedule_file(self):
#         file = self.cleaned_data['schedule_file']
#         from django.core.files.uploadedfile import InMemoryUploadedFile
#         return InMemoryUploadedFile()
#
#
#     def save(self):
#         pass