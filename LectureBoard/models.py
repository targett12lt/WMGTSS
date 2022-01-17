from tkinter import CASCADE
from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

# class LectureBoards(models.Model):  # Add this later, as this is dependent on what modules the student does
# Need to add a new requirement that the LectureBoard MUST be able to provide functionality to view more than one module's lectures 
# The lecture board must be able to show the appropriate modules to a student based upon their course.
#     Modules = models.  # Need to have a list of modules that the student does


class LectureBoard(models.Model):
    # Course_Identifier needs to be added here to support multiple modules per student 
    Course_Title = models.CharField(max_length=50)
    Course_Description = models.CharField(max_length=500)
    Course_Tutor = models.CharField(max_length=100)


class LectureDay(models.Model):
    LectureBoardFK = models.ForeignKey(LectureBoard, on_delete=models.CASCADE)  # Creating a many-to-one relationship with the LectureBoard object
    # LD_id = models.AutoField(primary_key=True)  # Creating auto-incrementing ID for the lecture day, shouldn't be needed as Django creates this itself - will delete later.
    Title = models.CharField(max_length=200)
    Description = models.CharField(max_length=500)  # Is 500 sufficient, test this
    Date = models.DateTimeField('Lecture Date')  # Not in original design, need to add to report/documentation
    LD_Img = models.ImageField(upload_to='LectureDayImgs') # Changed from a CharField to an Image field
    RelatedLectures = models.ManyToManyField()  # Check how to get a list here again


class SlidePack(models.Model):
    LectureDayFK = models.ForeignKey(LectureDay, on_delete=CASCADE)  # Creating a many-to-one relationship with the LectureDay object
    DownloadLink = models.CharField(max_length=200)  # Link to the file
    ProcSlidePack = models.CharField(max_length=200)  # Location of the slidepack

class VersionHistory(models.Model):
    SlidePackFK = models.ForeignKey(SlidePack, on_delete=CASCADE)  # Creating a many-to-one relationship with the SlidePack object
    ModDate = models.DateTimeField('Modification Date')
    VersionNum = models.IntegerField()
    Comment = models.CharField(max_length=300)

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

