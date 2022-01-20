from django.http import HttpResponse
from django.shortcuts import render
from .models import LectureBoard, LectureDay, SlidePack

# Create your views here.
def LectureBoardView(request):
    # module_lecture_days = ModuleBoard.objects.order_by('-Module Title')[:5]
    # output = ', '.join([q.Module_Title for q in module_lecture_days])
    # return HttpResponse(output)
    ModulesEnrolled = LectureBoard.objects.all()
    print('ModulesEnrolled:', ModulesEnrolled)
    context = {
        'ModulesEnrolled':ModulesEnrolled
    }
    return render(request, 'LectureBoard/LectureBoard.html', context)
    # Needs further work as just shows all modules currently, not what a student is registered to

def ModuleBoardView(request, req_Module_Code):
    '''Generates the Module Board View - requires the ModuleCode'''
    Module_PK = list(LectureBoard.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
    LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)
    output = ', '.join(q.Title for q in LectureList)
    context = {'LectureList': LectureList,
                'Module_Code': req_Module_Code}
    return render(request, 'LectureBoard/ModuleBoard.html', context)




def LectureDayView(request, req_Module_Code,lecture_id):
    Module_PK = list(LectureBoard.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
    # LectureInfo = 
    return HttpResponse('You have requested ' + req_Module_Code + ', in particular lecture ' + str(lecture_id))
    # recent_lecture = LectureDay.objects.get(id__exact=lecture_id)
    # return HttpResponse(recent_lecture.Title + ': ' + recent_lecture.Description)


