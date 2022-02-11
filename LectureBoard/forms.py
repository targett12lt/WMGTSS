from django import forms
from .models import Module, ModuleAccess, LectureDay, SlidePack, VersionHistory

class DateInput(forms.DateInput):
    input_type = 'date'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = "__all__"
        exclude = ['Module_Tutor']
        widgets = {
            'Module_Description': forms.Textarea
        }

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
        labels = {
            'OriginalFile': 'Slide Pack',
        }


class VersionHistoryForm(forms.ModelForm):   
    class Meta:
        model=VersionHistory
        fields = [
            'Comment',
            'VersionNum',
        ]

