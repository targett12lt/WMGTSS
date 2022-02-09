from django import forms
from .models import Module, LectureDay, SlidePack, VersionHistory
from crispy_forms.helper import FormHelper

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = "__all__"
        exclude = ['Module_Tutor']

class DateInput(forms.DateInput):
    input_type = 'date'

class LectureDayForm(forms.ModelForm):
    class Meta:
        model = LectureDay
        fields = "__all__"
        exclude = ['ModuleLectureBoard']
        widgets = {
            'Date': DateInput(),
            'Description': forms.Textarea
        }

class SlidePackForm(forms.ModelForm):
    class Meta:
        model = SlidePack
        fields= "__all__"
        exclude = ['LectureDay_FK', 'OnlineSlidePack']

class VersionHistoryForm(forms.ModelForm):   
    class Meta:
        model=VersionHistory
        fields = [
            'Comment',
            'VersionNum',
        ]

