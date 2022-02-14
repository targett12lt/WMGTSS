from django import forms
from .models import Module, LectureDay, SlidePack, VersionHistory

class DateInput(forms.DateInput):
    input_type = 'date'


class ModuleForm(forms.ModelForm):
    '''Form to allow Modules to be modified and created'''
    class Meta:
        model = Module
        fields = "__all__"
        exclude = ['Module_Tutor']
        widgets = {
            'Module_Description': forms.Textarea
        }

class LectureDayForm(forms.ModelForm):
    '''Form to allow Lecture Day's to be modified and created'''
    class Meta:
        model = LectureDay
        fields = "__all__"
        exclude = ['ModuleLectureBoard']
        widgets = {
            'Date': DateInput(),
            'Description': forms.Textarea
        }


class SlidePackForm(forms.ModelForm):
    '''Form to allow Slide Pack's to be modified and created'''
    class Meta:
        model = SlidePack
        fields= "__all__"
        exclude = ['LectureDay_FK', 'OnlineSlidePack']
        labels = {
            'OriginalFile': 'Slide Pack',
        }


class VersionHistoryForm(forms.ModelForm):
    '''Form to allow Version History objects to be modified and created'''
    class Meta:
        model=VersionHistory
        fields = [
            'Comment',
            'VersionNum',
        ]

