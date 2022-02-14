from django.test import TestCase

from .forms import ModuleForm

class NewModuleForm(TestCase):
    '''Tests that the New Module form shows the correct labels and fields'''
    def test_new_module_form_module_code(self):
        form = ModuleForm()
        self.assertTrue(form.fields['Module_Code'].label is None or form.fields['Module_Code'].label == 'Module Code')

    def test_new_module_form_module_title(self):
        form = ModuleForm()
        self.assertTrue(form.fields['Module_Title'].label is None or form.fields['Module_Title'].label == 'Module Title')

    def test_new_module_form_module_description(self):
        form = ModuleForm()
        self.assertTrue(form.fields['Module_Description'].label is None or form.fields['Module_Description'].label == 'Module Description')