from attr import attr, attrs
from django import forms
from matplotlib import widgets
from .models import Module, LectureDay, SlidePack, VersionHistory

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
            'ModDate',
        ]
        widgets = {
            'ModDate': DateInput(),
        }