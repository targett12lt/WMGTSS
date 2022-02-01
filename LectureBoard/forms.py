from django import forms
from .models import Module, LectureDay, SlidePack

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['Module_Code', 'Module_Title', 'Module_Description', 'Module_Tutor']
        