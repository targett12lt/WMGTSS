from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

# class LectureBoard(models.Model):  # Add this later, as this is dependent on what modules the student does
# Need to add a new requirement that the LectureBoard MUST be able to provide functionality to view more than one module's lectures 
# The lecture board must be able to show the appropriate modules to a student based upon their course.
#     Modules = models.  # Need to have a list of modules that the student does


class LectureBoard(models.Model):
    # Course_Identifier needs to be added here to support multiple modules per student 
    Module_Code = models.CharField(max_length=10)
    Module_Title = models.CharField(max_length=50)
    Module_Description = models.CharField(max_length=2000, blank=True)
    Module_Tutor = models.CharField(max_length=100, blank=True)

    def __str__(self):
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
    * ModuleLectureBoard (int) - Uses FK to create a many-to-one relationship with the LectureBoard object
    * id (int) - Used to identify the LectureDay
    * Title (char) - The title of the LectureDay, has a max length 200
    * Description (char) - This contains the description about the LectureDay, has a max length 2000
    * Date (datetime) - This stores the date/time that a LectureDay was presented
    * LD_Img(img) - Stores and hosts the LectureDay cover image using Django's FileSystemStorage class
    '''
    ModuleLectureBoard = models.ForeignKey(LectureBoard, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the LectureBoard object
    Title = models.CharField(max_length=200)
    Description = models.CharField(max_length=2000, blank=True)
    Date = models.DateTimeField('Lecture Date', blank=True)  # Not in original design, need to add to report/documentation
    LD_Img = models.ImageField(upload_to='LectureDayImgs', blank=True) # Changed from a CharField to an Image field

    def __str__(self):
        return self.Title   #Returns the title of the Lecture Day

    def description(self):
        return self.Description

    def get_img(self):
        return self.LD_Img

    def lecture_date(self):
        return self.lecture_date

class SlidePack(models.Model):
    LectureDayFK = models.ForeignKey(LectureDay, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the LectureDay object
    DownloadLink = models.CharField(max_length=200)  # Link to the file
    ProcSlidePack = models.CharField(max_length=200)  # Location of the slidepack

    def __str__(self):
        return self.DownloadLink

    def processed_deck(self):
        return self.ProcSlidePack


class VersionHistory(models.Model):
    SlidePackFK = models.ForeignKey(SlidePack, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the SlidePack object
    ModDate = models.DateTimeField('Modification Date')
    VersionNum = models.AutoField(primary_key=True)
    Comment = models.CharField(max_length=300, blank=True)


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

