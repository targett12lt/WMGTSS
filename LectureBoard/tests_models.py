from django.test import TestCase

from .models import Module, LectureDay, SlidePack, VersionHistory


class Module_ModelTests(TestCase):
    '''
    Creates a test object for Module model, ensures that all data is
    correctly populated and that empty query sets are returned correctly.
    '''
    
    def setUp(self):
        Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Creating a LB with all fields populated", Module_Tutor="Example")
    
    def test_create_Module_with_all_information(self):
        '''Checks that Module object has been created with correct information'''
        TestModule = Module.objects.get(Module_Code="WM001")
        self.assertEqual(TestModule.__str__(), "WM001")
        self.assertEqual(TestModule.title(), "TEST 1")
        self.assertEqual(TestModule.description(), "Creating a LB with all fields populated")
        self.assertEqual(TestModule.tutor(), "Example")

    def test_field_types(self):
        '''Testing all field types are the expected type'''
        self.assertIsInstance(Module.Module_Code, str)
        self.assertIsInstance(Module.Module_Title, str)
        self.assertIsInstance(Module.Module_Description, str)
        self.assertIsInstance(Module.Module_Tutor, str)

    def test_module_lookup(self):
        '''Tests that empty querysets are returned correctly'''
        self.assertFalse(Module.objects.get(Modle_Code="WM10987654").exists())


class LectureDay_ModelTests(TestCase):

    def example_func(self):
        pass


class SlidePack_ModelTests(TestCase):

    def example_func(self):
        pass


class VersionHistory_ModelTests(TestCase):

    def example_func(self):
        print("Hello world")

