from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import LectureBoard, LectureDay, SlidePack

# Create your views here.
def LectureBoardView(request):
    '''Generates a list of modules available to the user (currently shows all modules as it doesn't use a filter)'''
    ModulesEnrolled = LectureBoard.objects.all()
    print('ModulesEnrolled:', ModulesEnrolled)
    context = {
        'ModulesEnrolled':ModulesEnrolled
    }
    return render(request, 'LectureBoard/LectureBoard.html', context)
    # Needs further work as just shows all modules currently, not what a student is registered to

def ModuleBoardView(request, req_Module_Code):
    '''Generates the Module Board View - requires the ModuleCode'''
    try:
        ModuleCheck = LectureBoard.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(LectureBoard.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)
        output = ', '.join(q.Title for q in LectureList)
        context = {'LectureList': LectureList,
                    'Module_Code': req_Module_Code}
    except LectureBoard.DoesNotExist:
        raise Http404('The module requested: "' + req_Module_Code + '" does not exist.'
        '\n\nPlease contact your system administrator for further support.\n\n')
    
    return render(request, 'LectureBoard/ModuleBoard.html', context)




def LectureDayView(request, req_Module_Code,lecture_id):
    '''Provides a view for each lecture day.
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    * lecture_id = Auto-incrementing integer ID, PK for the lecture days, used to locate the lecture day and slidepack info
    '''
    
    # On this view, need to get LectureDay content: Title, Description and Date
    # Then need to get the slidepack informaiton, so: DownloadLink, ProcSlidePack
    # And finally can get the Version history for the slidepack (ModDate, VersionNum - this needs to be updated to autoincrement and the comment)
    
    # Checking if LectureDay exists and getting data:
    LectureDayInfo = get_object_or_404(LectureDay, id=lecture_id)  # Getting information about the lecture day using the ID from URL
    SlidePackInfo = SlidePack.objects.get(LectureDayFK = lecture_id)  # Getting slidepack info using lecture_id from URL as Foreign Key
    
    # Packaging all data from DB into context to load into HTML template:
    context = {
        'LectureDayInfo': LectureDayInfo,
        'SlidePackInfo': SlidePackInfo
        }

    return render(request, 'LectureBoard/LectureDay.html', context)
        



