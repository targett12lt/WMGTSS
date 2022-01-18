from django.http import HttpResponse
from .models import ModuleBoard

# Create your views here.
def LectureBoard(request):
    # module_lecture_days = ModuleBoard.objects.order_by('-Module Title')[:5]
    # output = ', '.join([q.Module_Title for q in module_lecture_days])
    # return HttpResponse(output)
    return HttpResponse('This is the Generic Lecture Board level which will show the modules a student is subscribed to')

def ModuleBoard(request, Module_Code):
    return HttpResponse("You have requested Lecture Board: %s" % Module_Code)

def LectureDay(request, Module_Code, lecture_identifier):
    return HttpResponse("You have requested day %s" % lecture_identifier)


