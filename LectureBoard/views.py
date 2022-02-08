from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Module, LectureDay, SlidePack
from .forms import ModuleForm, LectureDayForm, SlidePackForm, VersionHistoryForm

def check_Tutor_Group(user):
    if user:
        return user.groups.filter(name='Tutors').exists()
    return False

# Student Views:

@login_required
def Overview_StudentModules(request):
    '''Generates a list of modules available to the user (currently shows all modules as it doesn't use a filter)'''
    ModulesEnrolled = Module.objects.all()
    print('ModulesEnrolled:', ModulesEnrolled)
    context = {
        'ModulesEnrolled':ModulesEnrolled
    }
    return render(request, 'LectureBoard/Overview.html', context)
    # Needs further work as just shows all modules currently, not what a student is registered to

@login_required
def ModuleBoard_StudentView(request, req_Module_Code):
    '''Generates the Module Board View - requires the ModuleCode'''
    try:
        Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)
        context = {'LectureList': LectureList,
                    'Module_Info': Module_Info}
        print('Module Code:', req_Module_Code)
    except Module.DoesNotExist:
        raise Http404('The module requested: "' + req_Module_Code + '" does not exist.'
        '\n\nPlease contact your system administrator for further support.\n\n')
    
    return render(request, 'LectureBoard/ModuleBoard.html', context)

@login_required
def LectureDay_StudentView(request, req_Module_Code,lecture_id):
    '''Provides a view for each lecture day.
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    * lecture_id = Auto-incrementing integer ID, PK for the lecture days, used to locate the lecture day and slidepack info
    '''
    # And finally can get the Version history for the slidepack (ModDate, VersionNum - this needs to be updated to autoincrement and the comment)
    
    # Checking if LectureDay exists and getting data:
    LectureDayInfo = get_object_or_404(LectureDay, id=lecture_id)  # Getting information about the lecture day using the ID from URL
    SlidePackInfo = get_object_or_404(SlidePack, LectureDay_FK = lecture_id)  # Getting slidepack info using lecture_id from URL as Foreign Key
    
    # Packaging all data from DB into context to load into HTML template:
    context = {
        'LectureDayInfo': LectureDayInfo,
        'SlidePackInfo': SlidePackInfo
        }

    return render(request, 'LectureBoard/LectureDay.html', context)

# Tutor/edit views:

# --- Module Management (multiple) ---
@login_required
@user_passes_test(check_Tutor_Group)
def Overview_EditModules(request):
    '''Generates a list of modules available to the user (currently shows all modules as it doesn't use a filter)'''
    ModulesEnrolled = Module.objects.all()
    ModulesOwned = Module.objects.all()  # Update to ones only owned by tutor
    print('ModulesEnrolled:', ModulesEnrolled)
    context = {
        'ModulesEnrolled':ModulesEnrolled,
        'ModulesOwned': ModulesOwned,
    }
    return render(request, 'LectureBoard/OverviewEdit.html', context)
    # Needs further work as just shows all modules currently, not what a student is registered to

@login_required
@user_passes_test(check_Tutor_Group)
def Overview_NewModule(request):
    '''Provides the view to allow a Lecturer to add a new module to the DataBase.'''
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            NewModule = form.save(commit=False)
            NewModule.Module_Tutor = request.user
            NewModule.save()
            return redirect('Edit_Modules')
    else:
        form = ModuleForm()
    return render(request, 'LectureBoard/OverviewNew.html', {'form': form})


# --- Individual Module Management --- 
@login_required
@user_passes_test(check_Tutor_Group)
def Edit_Module(request, req_Module_Code):
    '''Generates the Module Board View - requires the ModuleCode'''
    try:
        Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)
        context = {'LectureList': LectureList,
                    'Module_Info': Module_Info}
        print('Module Code:', req_Module_Code)
    except Module.DoesNotExist:
        raise Http404('The module requested: "' + req_Module_Code + '" does not exist.'
        '\n\nPlease contact your system administrator for further support.\n\n')
    return render(request, 'LectureBoard/ModuleBoardEdit.html', context)

# --- Lecture Day Management ---
@login_required
@user_passes_test(check_Tutor_Group)
def Edit_LectureDay(request, req_Module_Code, lecture_id):
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
    SlidePackInfo = get_object_or_404(SlidePack, LectureDay_FK = lecture_id)  # Getting slidepack info using lecture_id from URL as Foreign Key
    
    # Packaging all data from DB into context to load into HTML template:
    context = {
        'LectureDayInfo': LectureDayInfo,
        'SlidePackInfo': SlidePackInfo
        }

    return render(request, 'LectureBoard/LectureDayEdit.html', context)


@login_required
@user_passes_test(check_Tutor_Group)
def New_LectureDay(request, req_Module_Code):
    ModuleInfo = get_object_or_404(Module, Module_Code=req_Module_Code)  # Getting information about the lecture day using the ID from URL
    if request.method == "POST":
        LDform = LectureDayForm(request.POST)
        SPForm = SlidePackForm(request.POST)
        VHForm = VersionHistoryForm
        if LDform.is_valid():
            NewLectureDay = LDform.save(commit=False)
            NewLectureDay.ModuleLectureBoard = ModuleInfo
            NewLectureDay.save()
            return redirect('Edit_Module', req_Module_Code)
    else:
        LDform = LectureDayForm()
    return render(request, 'LectureBoard/LectureDayNew.html', {'form': LDform})



    # OLD STUFF:
    
    # if request.method == "POST":
    #     LDform = LectureDayForm(request.POST)
    #     SPForm = SlidePackForm(request)
    #     VHForm = VersionHistoryForm

    #     if form.is_valid():
    #         NewModule = form.save(commit=False)
    #         NewModule.Module_Tutor = request.user
    #         NewModule.save()
    #         return redirect('Edit_Modules')
    # else:
    #     form = ModuleForm()
    # return render(request, 'LectureBoard/OverviewNew.html', {'form': form})


