from django.test import TestCase
from django.utils import timezone
from tables import Description
from .models import Module, LectureDay, SlidePack, VersionHistory


class Module_ModelTests(TestCase):
    '''
    Creates a test object for Module model, ensures that all data is
    correctly populated and that empty query sets are returned correctly.
    '''
    @classmethod
    def setUp(object):
        Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Creating a Module with all fields populated", Module_Tutor="Example")

    
    def test_create_LectureDay_with_all_information(self):
        '''Checks that LectureDay object has been created with correct information, using class methods'''
        TestModule = Module.objects.get(Module_Code="WM001")
        self.assertEqual(TestModule.__str__(), "WM001")
        self.assertEqual(TestModule.title(), "TEST 1")
        self.assertEqual(TestModule.description(), "Creating a Module with all fields populated")
        self.assertEqual(TestModule.tutor(), "Example")

    def test_module_code_label(self):
        '''Tests that the module code label hasn't changed'''
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('Module_Code').verbose_name
        self.assertEqual(field_label, 'Module Code')

    def test_module_code_length(self):
        '''Tests the maximum length of the module code hasn't changed'''
        module = Module.objects.get(id=1)
        max_length = module._meta.get_field('Module_Code').max_length
        self.assertEqual(max_length, 10)

    def test_module_title_label(self):
        '''Tests that the module code label hasn't changed'''
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('Module_Title').verbose_name
        self.assertEqual(field_label, 'Module Title')

    def test_module_title_length(self):
        '''Tests the maximum length of the module title hasn't changed'''
        module = Module.objects.get(id=1)
        max_length = module._meta.get_field('Module_Title').max_length
        self.assertEqual(max_length, 50)

    def test_module_description_label(self):
        '''Tests that the module code description label hasn't changed'''
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('Module_Description').verbose_name
        self.assertEqual(field_label, 'Module Description')

    def test_module_description_length(self):
        '''Tests the maximum length of the module description hasn't changed'''
        module = Module.objects.get(id=1)
        max_length = module._meta.get_field('Module_Description').max_length
        self.assertEqual(max_length, 2000)

    def test_module_description_blank(self):
        '''Tests that the module description field can be blank'''
        module = Module.objects.get(id=1)
        blank = module._meta.get_field('Module_Description').blank
        self.assertEqual(blank, True)

    def test_module_tutor_label(self):
        '''Tests that the module tutor label hasn't changed'''
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('Module_Tutor').verbose_name
        self.assertEqual(field_label, 'Module Tutor')

    def test_module_tutor_length(self):
        '''Tests the maximum length of the module tutor hasn't changed'''
        module = Module.objects.get(id=1)
        max_length = module._meta.get_field('Module_Tutor').max_length
        self.assertEqual(max_length, 100)

    def test_module_tutor_blank(self):
        '''Tests that the module description field can be blank'''
        module = Module.objects.get(id=1)
        blank = module._meta.get_field('Module_Tutor').blank
        self.assertEqual(blank, True)

    def test_get_absolute_url_view_only(self):
        '''Tests to ensure that the URL has been defined for the Module'''
        module = Module.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(module.get_absolute_url_view_only(), '/LectureBoard/WM001/')
    
    def test_get_absolute_url_edit(self):
        '''Tests to ensure that the URL has been defined for the Module'''
        module = Module.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(module.get_absolute_url_edit(), '/LectureBoard/WM001/edit/')


class LectureDay_ModelTests(TestCase):
    '''
    Creates a test object for Module model, ensures that all data is
    correctly populated and that empty query sets are returned correctly.
    '''
    date_time = timezone.now()  # Getting a datetime value to test with 

    @classmethod
    def setUp(object):
        module = Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Creating a Module with all fields populated", Module_Tutor="Example")
        
        LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing", Description="Object to test LD object",
        Date = LectureDay_ModelTests.date_time)

    

    def test_create_Lectureday_with_all_information(self):
        '''Checks that Module object has been created with correct information, using class methods'''
        TestLectureDay = LectureDay.objects.get(Module_Code="WM001")
        self.assertEqual(TestLectureDay.__str__(), "LectureDay Testing")
        self.assertEqual(TestLectureDay.description(), "Creating a Module with all fields populated")
        self.assertEqual(TestLectureDay.lecture_date(), "01/01/2022 12:05:00")

    def test_ModuleLectureBoard_label(self):
        '''Tests that the ModuleLectureBoard label hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        field_label = lectureday._meta.get_field('ModuleLectureBoard').verbose_name
        self.assertEqual(field_label, 'ModuleLectureBoard')
    
    def test_title_label(self):
        '''Tests that the Title label hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        field_label = lectureday._meta.get_field('Title').verbose_name
        self.assertEqual(field_label, 'Title')
    
    def test_title_length(self):
        '''Tests the maximum length of the title field hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        max_length = lectureday._meta.get_field('Title').max_length
        self.assertEqual(max_length, 200)
    
    def test_description_label(self):
        '''Tests that the description label hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        field_label = lectureday._meta.get_field('Description').verbose_name
        self.assertEqual(field_label, 'Description')
    
    def test_description_length(self):
        '''Tests the maximum length of the description field hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        max_length = lectureday._meta.get_field('Description').max_length
        self.assertEqual(max_length, 2000)
    
    def test_description_blank(self):
        '''Tests that the lectureday description field can be blank'''
        lectureday = LectureDay.objects.get(id=1)
        blank = lectureday._meta.get_field('Description').blank
        self.assertEqual(blank, True)

    def test_date_label(self):
        '''Tests that the description label hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        field_label = lectureday._meta.get_field('Date').verbose_name
        self.assertEqual(field_label, 'Lecture Date')
    
    def test_date_blank(self):
        '''Tests the maximum length of the description field hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        blank = lectureday._meta.get_field('Date').blank
        self.assertEqual(blank, True)
    
    def test_get_absolute_url_view_only(self):
        '''Tests to ensure that the URL has been defined for the Module'''
        lectureday = LectureDay.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(lectureday.get_absolute_url_view_only(), '/LectureBoard/WM001/')
        
    def test_get_absolute_url_edit(self):
        '''Tests to ensure that the URL has been defined for the Module fir editing'''
        lectureday = LectureDay.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(lectureday.get_absolute_url_edit(), '/LectureBoard/WM001/')


class SlidePack_ModelTests(TestCase):
    '''
    Creates a test object for Module model, ensures that all data is
    correctly populated and that empty query sets are returned correctly.
    '''
    date_time = timezone.now()  # Getting a date_time value to test with

    @classmethod
    def setUp(object):
        module = Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Creating a Module with all fields populated", Module_Tutor="Example")
        
        LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing", Description="Object to test LD object",
        Date = LectureDay_ModelTests.date_time)
    

    def test_create_Lectureday_with_all_information(self):
        '''Checks that Module object has been created with correct information, using class methods'''
        TestLectureDay = LectureDay.objects.get(Module_Code="WM001")
        self.assertEqual(TestLectureDay.__str__(), "LectureDay Testing")
        self.assertEqual(TestLectureDay.description(), "Creating a Module with all fields populated")
        self.assertEqual(TestLectureDay.lecture_date(), "01/01/2022 12:05:00")

    def test_ModuleLectureBoard_label(self):
        '''Tests that the ModuleLectureBoard label hasn't changed'''
        lectureday = LectureDay.objects.get(id=1)
        field_label = lectureday._meta.get_field('ModuleLectureBoard').verbose_name
        self.assertEqual(field_label, 'ModuleLectureBoard')

    def test_check_file_type(self):
        pass

    def test_check_file_size(self)@
        pass


class VersionHistory_ModelTests(TestCase):

    def example_func(self):
        print("Hello world")

