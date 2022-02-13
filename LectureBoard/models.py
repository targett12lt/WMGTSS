import os
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse
from datetime import datetime


class Module(models.Model):
    '''
    This class represents a given (university) Module.
    
    Attributes:
    * id (int) - Used to uniquely identify the Module (Primary Key)
    * Module_Code (char) - The code of the University Module, has a max length of 10.
    * Module_Title (char) - The title of the Module, has a max length 50.
    * Module_Description (char) - This contains the description about the Module, has a max length 2000.
    * Module_Tutor (char) - This says who is teaching the Module, has a max length 100.
    '''

    Module_Code = models.CharField(max_length=10)
    Module_Title = models.CharField(max_length=50)
    Module_Description = models.CharField(max_length=2000, blank=True)
    Module_Tutor = models.ForeignKey(User, verbose_name='Module Tutor', on_delete=models.CASCADE)  # Using Djano's built in user method so they own it.

    def __str__(self):
        return self.Module_Code
    
    def title(self):
        return self.Module_Title

    def description(self):
        return self.Module_Description

    def tutor(self):
        return self.Module_Tutor

    def get_absolute_url_view_only(self):
        return reverse('ModuleBoard', args=[str(self.Module_Code)])
    
    def get_absolute_url_edit(self):
        return reverse('ModuleBoardTutor', args=[str(self.Module_Code)])    

class ModuleAccess(models.Model):
    '''
    This class stores the data about the user groups who can access a given university module
    
    Attributes:
    * id (int) - Used to uniquely identify the Module Access Model (Primary Key)
    * Module_Identifier (Module) - Used to identify the parent model that the Module Access item relates to. 
      A FK is used to create a ONE-TO-MANY relationship with the Module object.
    * UserGroup (char) - String of user group name
    '''
    Module_Identifier = models.ForeignKey(Module, on_delete=models.CASCADE)
    UserGroupName = models.CharField(max_length=50)

    def __str__(self):
        return self.UserGroupName
    
    def ModuleGivenAccessTo(self):
        return self.Module_Identifier


class LectureDay(models.Model):
    '''
    This class represents a given LectureDay for a module (relationship can be identified using the FK).
    
    Each University Module has a MANY-TO-ONE relationship with the LectureDay object.
    
    Attributes:
    * id (int) - Used to identify the LectureDay (Primary Key)
    * ModuleLectureBoard (int) - Uses FK to create a ONE-TO-MANY relationship with the Module object
    * Title (char) - The title of the LectureDay, has a max length 200
    * Description (char) - This contains the description about the LectureDay, has a max length 2000
    * Date (datetime) - This stores the date/time that a LectureDay was presented
    * LD_Img(img) - Stores and hosts the LectureDay cover image using Django's FileSystemStorage class
    '''

    ModuleLectureBoard = models.ForeignKey(Module, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the Module object
    Title = models.CharField(max_length=200)
    Description = models.CharField(max_length=2000, blank=True)
    Date = models.DateTimeField('Lecture Date', blank=True, default=datetime.now)  # Not in original design, need to add to report/documentation
    LD_Img = models.ImageField(upload_to='LectureDayImgs', blank=True) # Changed from a CharField to an Image field

    def __str__(self):
        return self.Title   #Returns the title of the Lecture Day
    
    def get_module_code(self):
        return self.ModuleLectureBoard.Module_Code

    def description(self):
        return self.Description

    def get_img(self):
        return self.LD_Img

    def lecture_date(self):
        return self.Date
    
    def get_absolute_url_view_only(self):
        '''For student/view-only site'''
        return reverse('LectureDay', args=[str(self.get_module_code()), int(self.id)])

    def get_absolute_url_edit(self):
        '''For editing/lecture site'''
        return reverse('Edit_LectureDay', args=[str(self.get_module_code()), int(self.id)])


class Data_Validators():
    '''
    Stores the SlidePack methods, includes the following methods:
    * validate_file_extension - Ensures that only the correct file types are uploaded
    * validate_file_size - Ensures that the file is under the desired limit (50 MB)
    '''

    def validate_file_extension(value):
        '''
        Ensures that only the correct file types are uploaded by validating the file is a PPTX or PPT File format.
        The file should be passed to the fuction using the 'value' parameter.
        '''
        ext = os.path.splitext(value.name)[1]
        allowed_extensions = ['.pptx', '.ppt']
        if not ext in allowed_extensions:
            raise ValidationError(u'File type not allowed - Please choose another file!')

    def validate_file_size(value):
        '''
        Validates that the file is under 50 MB - this is the maximum file size which can be uploaded.
        The file is passed to the function using the 'value' parameter.
        '''
        file_size = value.size

        if file_size > 52428800:  # 50MB in Bytes
            raise ValidationError(u"This file has exceeded the 50MB size limit - Please choose another file!")


class SlidePack(models.Model):
    '''
    This class represents a given SlidePack for a LectureDay (relationship can be identified using the FK).
    
    Each Lecture Day has a ONE-TO-ONE relationship with the SlidePack object.
    
    Attributes:
    * id (int) - Used to identify the SlidePack (Primary Key)
    * LectureDayFK (LectureDay object) - Uses FK to create a ONE-TO-ONE relationship with the Module object.
    * OriginalFile (file) - Usees Django file management system to upload and store PPT/PPTX Files in a designated folder 
    (set using the 'upload_to' argument).
    * OnlineSlidePack (file) - Usees Django file management system to store PDF Files in a designated folder 
    (set using the 'upload_to' argument), after the PPT/PPTX file has been processed (so it can be viewed in Browser).
    '''
    
    LectureDay_FK = models.OneToOneField(LectureDay, on_delete=models.CASCADE)  # Creating a one-to-one relationship with the LectureDay object
    OriginalFile = models.FileField(upload_to='SlidePacks/original', blank=True, validators=[Data_Validators.validate_file_extension, Data_Validators.validate_file_size])  # Original .PPT, .PPTX file - NEED TO MAKE THIS DYNAMIC FILE PATH IN LATER ITERATION
    OnlineSlidePack = models.FileField(upload_to='SlidePacks/online', blank=True)  # Converted slidepack in .PDF format to view in browser - AGAIN THIS NEEDS TO BE MADE DYNAMIC TOO
    SlidePack_id = models.AutoField(verbose_name="ID", primary_key=True)

    def identifier(self):
        '''Returns the SlidePack Identifier'''
        return self.SlidePack_id
    
    def original_file(self):
        '''Returns the file that the user originally uploaded'''
        return os.path.basename(self.OriginalFile.name)
    
    def online_slide_pack(self):
        '''Returns the processed slide pack, which is used for online viewing'''
        return self.OnlineSlidePack

    def paired_lectureday(self):
        '''Returns the LectureDay object of the SlidePack'''
        return self.LectureDay_FK
    
    def get_Module_Code(self):
        '''Returns the module Code for the LectureDay'''
        return self.LectureDay_FK.get_module_code()

    def get_absolute_url_view_only(self):
        '''For student/view-only site'''
        return reverse('LectureDay', args=[str(self.get_module_code()), int(self.id)])

    def get_absolute_url_edit(self):
        '''For editing/lecture site'''
        return reverse('Edit_LectureDay', args=[str(self.get_module_code()), int(self.id)])

    def delete(self):
        '''Deletes the original (OriginalFile) PPT/PPTX and processed PDF'''
        self.OriginalFile.delete()
        self.OnlineSlidePack.delete()


class VersionHistory(models.Model):
    '''
    This class represents a given SlidePack's 'Version History' (relationship can be identified using the FK).
    
    Each SlidePack Day has a ONE-TO-MANY relationship with the Version History objects.
    
    Attributes:
    * id (int) - Used to identify the VersionHistory (Primary Key)
    * SlidePackFK (SlidePack object) - Uses FK to create a ONE-TO-ONE relationship with the Module object.
    * ModDate (date time) - Stores the time when the file was modified/updated.
    * VersionNum (int) - Used to identify a version of the SlidePack, 
    automatically increases by +1 each time a new file is uploaded (used as PK).
    * Comment (char) - Allows a comment to be made about the new version of the 
    SlidePack with a maximum length of 300 (can be left blank).
    '''
    
    SlidePackFK = models.ForeignKey(SlidePack, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the SlidePack object
    ModDate = models.DateTimeField('Modification Date')
    VersionNum = models.PositiveSmallIntegerField('')
    Comment = models.CharField(max_length=300, blank=True, verbose_name='')

    def identifier(self):
        return self.VersionNum
    
    def paired_slidePack(self):
        return self.SlidePackFK
    
    def date_modified(self):
        return self.ModDate

    def comment(self):
        return self.Comment

