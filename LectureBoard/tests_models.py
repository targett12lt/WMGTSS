from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User

import mock
import os
import glob

from .models import Module, LectureDay, SlidePack, VersionHistory, Data_Validators


class Module_ModelTests(TestCase):
    '''
    Creates a test object for Module model, ensures that all data is
    populated and that field names, types, and limits are correct.
    '''
    @classmethod
    def setUp(object):
        user_1 = User.objects.create_user('John Smith', 'John@smith.com', 'JSPassword')
        Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Creating a Module with all fields populated", Module_Tutor=user_1)

    
    def test_check_Module_with_all_information(self):
        '''Checks that Module object has been created with correct information, using class methods'''
        TestModule = Module.objects.get(Module_Code="WM001")
        self.assertEqual(TestModule.__str__(), "WM001")
        self.assertEqual(TestModule.title(), "TEST 1")
        self.assertEqual(TestModule.description(), "Creating a Module with all fields populated")

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
    Creates a test object for LectureDay model, ensures that all data is
    populated and that field names, types, and limits are correct.

    No need to test if can exist without Module, Parent-Child relationship means
    it will automatically be deleted if parent is.
    '''
    
    current_time = timezone.now()  # Getting a datetime value to test with 
    
    @classmethod
    def setUp(object):
        user_1 = User.objects.create_user('John Smith', 'John@smith.com', 'JSPassword')
        module = Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Object to test LD object", Module_Tutor=user_1)
        
        LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing", Description="Object to test LD object",
        Date = LectureDay_ModelTests.current_time)

    def test_check_Lectureday_with_all_information(self):
        '''Checks that LectureDay object has been created with correct information, using class methods'''
        TestLectureDay = LectureDay.objects.get(Title="LectureDay Testing")
        self.assertEqual(TestLectureDay.__str__(), "LectureDay Testing")
        self.assertEqual(TestLectureDay.description(), "Object to test LD object")
        self.assertEqual(TestLectureDay.lecture_date(), self.current_time)

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
        '''Tests to ensure that the URL has been defined for the LectureDay'''
        lectureday = LectureDay.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(lectureday.get_absolute_url_view_only(), '/LectureBoard/WM001/1/')
        
    def test_get_absolute_url_edit(self):
        '''Tests to ensure that the URL has been defined for the LectureDay for editing'''
        lectureday = LectureDay.objects.get(id=1)
        # This will also fail if it hasn't been defined:
        self.assertEqual(lectureday.get_absolute_url_edit(), '/LectureBoard/WM001/1/edit/')


class SlidePack_ModelTests(TestCase):
    '''
    Creates a test object for SlidePack model, ensures that all data is
    populated and that field names, types, and limits are correct.

    No need to test if can exist without LectureDay, Parent-Child relationship means
    it will automatically be deleted if parent is.
    '''
    # Class Variables:
    current_time = timezone.now()
    mock_file = mock.MagicMock(spec=File)
    mock_file.name = 'testing.pptx'
    processed_mock_file = mock.MagicMock(spec=File)
    processed_mock_file.name = 'testing.pdf'

    @classmethod
    def setUp(object):
        user_1 = User.objects.create_user('John Smith', 'John@smith.com', 'JSPassword')
        module = Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Object to test SP object", Module_Tutor=user_1)
        
        lectureday = LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing", Description="Object to test SP object",
        Date = SlidePack_ModelTests.current_time)

        SlidePack.objects.create(LectureDay_FK = lectureday)

        #Creating SlidePack Object with Files attached:
        lectureday2 = LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing2", Description="Object to test SP object2",
        Date = SlidePack_ModelTests.current_time)
        
        SlidePack.objects.create(LectureDay_FK = lectureday2,
        OriginalFile=SlidePack_ModelTests.mock_file, 
        OnlineSlidePack=SlidePack_ModelTests.processed_mock_file)         

    def test_create_Lectureday_with_all_information(self):
        '''Checks that Module object has been created with correct information, using class methods'''
        TestSlidePack = SlidePack.objects.get(LectureDay_FK = LectureDay.objects.get(id=1))
        self.assertEqual(TestSlidePack.identifier(), 1)

    def test_LectureDayFK_label(self):
        '''Tests that the SlidePackFK label hasn't changed'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        field_label = slidepack._meta.get_field('LectureDay_FK').verbose_name
        self.assertEqual(field_label, 'LectureDay FK')
    
    def test_SlidePackID_label(self):
        '''Tests that the SlidePackID label hasn't changed'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        field_label = slidepack._meta.get_field('SlidePack_id').verbose_name
        self.assertEqual(field_label, 'ID')
    
    def test_OriginalFile_label(self):
        '''Tests that the OriginalFile label hasn't changed'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        field_label = slidepack._meta.get_field('OriginalFile').verbose_name
        self.assertEqual(field_label, 'OriginalFile')
    
    def test_OriginalFile_blank(self):
        '''Tests that the Original File field allows no input'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        blank = slidepack._meta.get_field('OriginalFile').blank
        self.assertEqual(blank, True)

    def test_OnlineSlidePack_label(self):
        '''Tests that the OnlineSlidePack label hasn't changed'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        field_label = slidepack._meta.get_field('OnlineSlidePack').verbose_name
        self.assertEqual(field_label, 'OnlineSlidePack')
    
    def test_OnlineSlidePack_blank(self):
        '''Tests that the OnlineSlidePack label hasn't changed'''
        slidepack = SlidePack.objects.get(SlidePack_id=1)
        blank = slidepack._meta.get_field('OnlineSlidePack').blank
        self.assertEqual(blank, True)

    def test_upload_original_file(self):
        '''Creates a mock file to be used in the OriginalFile field'''
        file_model = SlidePack(OriginalFile=self.mock_file)
        # Testing:
        self.assertEqual(file_model.OriginalFile.name, self.mock_file.name)
    
    def test_upload_processed_file(self):
        '''Creates a mock file to be used in the OnlineSlidePack field'''
        # Getting file model:
        file_model = SlidePack(OnlineSlidePack=self.processed_mock_file)
        # Testing:
        self.assertEqual(file_model.OnlineSlidePack.name, self.processed_mock_file.name)

    def test_check_file_type(self):
        '''Checking that the validator blocks incorrect file types when 
        supplied with file type which is not a .PPT/.PPTX'''
        wrong_file_type = False
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = 'testing.txt'
        try:
            Data_Validators.validate_file_extension(mock_file)
            wrong_file_type = False
        except ValidationError:
            wrong_file_type = True
        self.assertTrue(wrong_file_type)

    def wip_test_check_file_size(self):
        '''Checking that the validator only allows files under 50 MB to be 
        uploaded
        
        NOT SURE HOW TO DO THIS YET, NEEDS TO BE FIXED
        '''
        pass

    def test_delete__slidepacks(self):
        '''Deletes both the original slidepack and the processed slidepack created for testing'''
        slidepack_testing = SlidePack.objects.get(SlidePack_id = 2)
        SlidePack.delete(slidepack_testing)
        success = False
        if bool(slidepack_testing.OriginalFile) == False:
            if bool(slidepack_testing.OnlineSlidePack) == False:
                success = True
        return success


class VersionHistory_ModelTests(TestCase):
    """
    Creates a test object for SlidePack model, ensures that all data is
    populated and that field names, types, and limits are correct.

    No need to test if can exist without SlidePack, Parent-Child relationship means
    it will automatically be deleted if parent is.
    """
    # Class Variables:
    current_time = timezone.now()
    mock_file = mock.MagicMock(spec=File)
    mock_file.name = 'testing.pptx'
    processed_mock_file = mock.MagicMock(spec=File)
    processed_mock_file.name = 'testing.pdf'

    @classmethod
    def setUp(object):       
        user_1 = User.objects.create_user('John Smith', 'John@smith.com', 'JSPassword')
        module = Module.objects.create(Module_Code="WM001", Module_Title="TEST 1",
        Module_Description="Object to test SP object", Module_Tutor=user_1)
        
        lectureday = LectureDay.objects.create(ModuleLectureBoard = module, 
        Title="LectureDay Testing", Description="Object to test SP object",
        Date = VersionHistory_ModelTests.current_time)

        slidepack = SlidePack.objects.create(LectureDay_FK = lectureday, 
        OriginalFile=VersionHistory_ModelTests.mock_file, 
        OnlineSlidePack= VersionHistory_ModelTests.processed_mock_file)

        VersionHistory.objects.create(SlidePackFK = slidepack, 
        ModDate = VersionHistory_ModelTests.current_time, VersionNum = int(1),
        Comment = "Testing Comment")


    def test_check_VersionHistory_has_all_information(self):
        '''Checks that the VersionHistory object has been created with correct 
        information, using the class method'''
        TestVersionHistory = VersionHistory.objects.get(SlidePackFK = SlidePack.objects.get(SlidePack_id=1))
        self.assertEqual(TestVersionHistory.identifier(), int(1))
        self.assertEqual(TestVersionHistory.date_modified(), self.current_time)
        self.assertEqual(TestVersionHistory.comment(), "Testing Comment")


def tearDownModule():
    ''' Tidies up any old files from testing'''
    cwd = os.getcwd()
    online_folder = os.path.join(cwd, 'media\\SlidePacks\\online\\')
    original_folder = os.path.join(cwd, 'media\\SlidePacks\\original\\')
    for filename in os.listdir(original_folder):
        if filename.startswith('testing'):
            os.remove(os.path.join(original_folder, filename))
    for filename in os.listdir(online_folder):
        if filename.startswith('testing'):
            os.remove(os.path.join(online_folder, filename))


