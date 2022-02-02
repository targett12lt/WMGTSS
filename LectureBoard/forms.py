from django import forms
from .models import Module, LectureDay, SlidePack

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = "__all__"
        exclude = ['Module_Tutor']


class LectureForm(forms.ModelForm):
    class Meta:
        model = LectureDay
        slidepack_model = SlidePack
        fields = "__all__"
        exclude = ['ModuleLectureBoard']

