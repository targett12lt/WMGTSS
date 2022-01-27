import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.forms import ValidationError

# Create your models here.

# class LectureBoard(models.Model):  # Add this later, as this is dependent on what modules the student does
# Need to add a new requirement that the LectureBoard MUST be able to provide functionality to view more than one module's lectures 
# The lecture board must be able to show the appropriate modules to a student based upon their course.
#     Modules = models.  # Need to have a list of modules that the student does


class Module(models.Model):
    '''
    This class represents a given (university) Module.
    
    Attributes:
    * id (int) - Used to identify the Module
    * Module_Code (char) - The code of the University Module, has a max length of 10.
    * Module_Title (char) - The title of the Module, has a max length 50.
    * Module_Description (char) - This contains the description about the Module, has a max length 2000.
    * Module_Tutor (char) - This says who is teaching the Module, has a max length 100.
    '''

    Module_Code = models.CharField(max_length=10)
    Module_Title = models.CharField(max_length=50)
    Module_Description = models.CharField(max_length=2000, blank=True)
    Module_Tutor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.Module_Code
    
    def title(self):
        return self.Module_Title

    def description(self):
        return self.Module_Description

    def tutor(self):
        return self.Module_Tutor


class LectureDay(models.Model):
    '''
    This class represents a given LectureDay for a module (relationship can be identified using the FK).
    
    Each University Module has a MANY-TO-ONE relationship with the LectureDay object.
    
    Attributes:
    * ModuleLectureBoard (int) - Uses FK to create a many-to-one relationship with the Module object
    * id (int) - Used to identify the LectureDay
    * Title (char) - The title of the LectureDay, has a max length 200
    * Description (char) - This contains the description about the LectureDay, has a max length 2000
    * Date (datetime) - This stores the date/time that a LectureDay was presented
    * LD_Img(img) - Stores and hosts the LectureDay cover image using Django's FileSystemStorage class
    '''

    ModuleLectureBoard = models.ForeignKey(Module, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the Module object
    Title = models.CharField(max_length=200)
    Description = models.CharField(max_length=2000, blank=True)
    Date = models.DateTimeField('Lecture Date', blank=True)  # Not in original design, need to add to report/documentation
    LD_Img = models.ImageField(upload_to='content/LectureDayImgs', blank=True) # Changed from a CharField to an Image field

    def __str__(self):
        return self.Title   #Returns the title of the Lecture Day
    
    def get_module_code(self):
        # NEED TO DO THIS
        return "Hello world!"

    def description(self):
        return self.Description

    def get_img(self):
        return self.LD_Img

    def lecture_date(self):
        return self.lecture_date

class SlidePackMethods():
#    This could be changed to this location: http://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php
    '''
    Stores the SlidePack methods, includes the following methods:
    * validate_file_extension - Ensures that only the correct file types are uploaded
    * convert_file_to_pdf - Converts the PPTX/PPT to PDF so file can be viewed in Browser
    * update_ver_history - Updates the Version History of a Slide Pack when a new version of a slide pack is uploaded to the LectureBoard.
    '''

    def validate_file_extension(value):
        '''Validates the file is a PPTX or PPT File format. The file should be passed to the fuction using the 'value' parameter.'''
        ext = os.path.splitext(value.name)[1]
        allowed_extensions = ['.pptx', '.ppt']
        if not ext in allowed_extensions:
            raise ValidationError(u'File type not allowed - Please choose another file!')

    def validate_file_size(value):
        '''Validates that the file is under 50 MB - this is the maximum file size which can be uploaded. The file is passed to the function using the 'value' parameter.'''
        file_size = value.size

        if file_size > 52428800:  # 50MB in Bytes
            raise ValidationError(u"This file has exceeded the 50MB size limit - Please choose another file!")

    def convert_file_to_pdf():
        '''Converts the PPT/PPTX file to PDF format so that it can be viewed in the BootStrap Browser Front-end'''
        print('Hello World!')

    def update_ver_history():
        '''Updates the version history for a given slide pack, allowing the user to provide a description and automatically increments the Version number'''
        print("Hello again from the version history :)")


class SlidePack(models.Model):
    '''
    This class represents a given SlidePack for a LectureDay (relationship can be identified using the FK).
    
    Each Lecture Day has a ONE-TO-ONE relationship with the SlidePack object.
    
    Attributes:
    * LectureDayFK (int) - Uses FK to create a one-to-one relationship with the Module object.
    * id (int) - Used to identify the SlidePack.
    * OriginalFile (file) - Usees Django file management system to upload and store PPT/PPTX Files in a designated folder 
    (set using the 'upload_to' argument).
    * OnlineSlidePack (file) - Usees Django file management system to store PDF Files in a designated folder 
    (set using the 'upload_to' argument), after the PPT/PPTX file has been processed (so it can be viewed in Browser).
    '''
    
    LectureDay_FK = models.OneToOneField(LectureDay, on_delete=models.CASCADE, primary_key=True)  # Creating a one-to-one relationship with the LectureDay object
    OriginalFile = models.FileField(upload_to='LectureBoard/content/SlidePacks/original', blank=True, validators=[SlidePackMethods.validate_file_extension, SlidePackMethods.validate_file_size])  # Original .PPT, .PPTX file - NEED TO MAKE THIS DYNAMIC FILE PATH IN LATER ITERATION
    OnlineSlidePack = models.FileField(upload_to='LectureBoard/content/SlidePacks/online', blank=True)  # Converted slidepack in .PDF format to view in browser - AGAIN THIS NEEDS TO BE MADE DYNAMIC TOO


class VersionHistory(models.Model):
    '''
    This class represents a given SlidePack's 'Version History' (relationship can be identified using the FK).
    
    Each SlidePack Day has a ONE-TO-MANY relationship with the Version History objects.
    
    Attributes:
    * SlidePackFK (int) - Uses FK to create a one-to-one relationship with the Module object.
    * ModDate (date time) - Stores the time when the file was modified/updated.
    * VersionNum (int) - Used to identify a version of the SlidePack, 
    automatically increases by +1 each time a new file is uploaded (used as PK).
    * Comment (char) - Allows a comment to be made about the new version of the 
    SlidePack with a maximum length of 300 (can be left blank).
    '''
    
    SlidePackFK = models.ForeignKey(SlidePack, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the SlidePack object
    ModDate = models.DateTimeField('Modification Date')
    VersionNum = models.AutoField(primary_key=True)
    Comment = models.CharField(max_length=300, blank=True)

