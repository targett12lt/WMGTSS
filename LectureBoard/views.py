import os

# Importing objects from other modules:
from .models import Module, LectureDay, SlidePack, VersionHistory
from .forms import ModuleForm, LectureDayForm, SlidePackForm, VersionHistoryForm
from .processing import PPT_Convert

# Importing required django modules:
from django.http import Http404
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q


def check_Tutor_Group(user):
    if user:
        return user.groups.filter(name='Tutors').exists()
    return False

# Student Views:

@login_required
def Overview_StudentModules(request):
    '''Generates a list of modules available to the user (currently shows all modules as it doesn't use a filter)'''
    ModulesEnrolled = Module.objects.all()
    context = {
        'SearchFunctionality': True,
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
        context = {
            'SearchFunctionality': True,
            'LectureList': LectureList,
            'Module_Info': Module_Info}
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
        'SearchFunctionality': True,
        'LectureDayInfo': LectureDayInfo,
        'SlidePackInfo': SlidePackInfo
        }

    return render(request, 'LectureBoard/LectureDay.html', context)

# Tutor/edit views:

# --- Module Management (multiple) ---
@user_passes_test(check_Tutor_Group)
def Overview_Tutor(request):
    '''Generates a list of modules available to the user (currently shows all modules as it doesn't use a filter)'''
    ModulesEnrolled = Module.objects.all()
    ModulesOwned = Module.objects.filter(Module_Tutor=request.user)  # Shows only modules that they own
    context = {
        'SearchFunctionality':True,
        'ModulesEnrolled':ModulesEnrolled,
        'ModulesOwned': ModulesOwned,
    }
    return render(request, 'LectureBoard/OverviewTutor.html', context)
    # Needs further work as just shows all modules currently, not what a student is registered to

@user_passes_test(check_Tutor_Group)
def New_Module(request):
    '''Provides the view to allow a Lecturer to add a new module to the Database.'''
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            NewModule = form.save(commit=False)
            NewModule.Module_Tutor = request.user
            NewModule.save()
            return redirect('Overview_Tutor')
    else:
        form = ModuleForm()
    return render(request, 'LectureBoard/Overview_NewModule.html', {'form': form})


@user_passes_test(check_Tutor_Group)
def Edit_Module(request, req_Module_Code):
    '''Provides the view to allow a Lecturer to add a new module to the Database.'''
    ModuleInstance = Module.objects.get(Module_Code = req_Module_Code)
    form = ModuleForm(request.POST or None, instance=ModuleInstance)
    if form.is_valid():
        NewModule = form.save(commit=False)
        NewModule.Module_Tutor = request.user
        NewModule.save()
        return redirect('Overview_Tutor')
    return render(request, 'LectureBoard/Overview_EditModule.html', {'form': form})


def Delete_Module(request, req_Module_Code):
    query = Module.objects.get(Module_Code=req_Module_Code)
    query.delete()
    return redirect('Overview_Tutor')


# --- Individual Module Management --- 
@user_passes_test(check_Tutor_Group)
def ModuleBoardTutor(request, req_Module_Code):
    '''Generates the Module Board View - requires the ModuleCode'''
    try:
        Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)
        context = {
                'SearchFunctionality': True,
                'LectureList': LectureList,
                'Module_Info': Module_Info
        }
    except Module.DoesNotExist:
        raise Http404('The module requested: "' + req_Module_Code + '" does not exist.'
        '\n\nPlease contact your system administrator for further support.\n\n')
    return render(request, 'LectureBoard/ModuleBoardTutor.html', context)

# --- Lecture Day Management ---
@user_passes_test(check_Tutor_Group)
def Edit_LectureDay(request, req_Module_Code, lecture_id):  
    '''Provides the view to allow a Lecturer to modify an existing modify on the Database.'''
    
    LDInstance = get_object_or_404(LectureDay, pk=lecture_id)
    SPInstance = get_object_or_404(SlidePack, LectureDay_FK=LDInstance)

    Previous_Version_History = None
    
    # Trying to check if it has any version history
    try:
        Previous_Version_History = VersionHistory.objects.filter(SlidePackFK = SPInstance)
    except Exception as e:
        pass

    LDForm = LectureDayForm(request.POST or None, request.FILES or None, instance=LDInstance)
    SPForm = SlidePackForm(request.POST or None, request.FILES or None, instance=SPInstance)
    VHForm = VersionHistoryForm(request.POST or None, request.FILES or None)
    context = {
        'LDForm': LDForm,
        'SPForm': SPForm,
        'VHForm': VHForm,
        'Previous_Version_History': Previous_Version_History,
        'current_date': timezone.now(),
    }
    if LDForm.is_valid():
        ModifiedLectureDay = LDForm.save(commit=False)
        ModifiedLectureDay.save()
        if SPForm.is_valid():
            ModifiedSlidePack = SPForm.save(commit=False)
            ModifiedSlidePack.save()
            if VHForm.is_valid():
                NewVersionHistoryEntry = VHForm.save(commit=False)
                NewVersionHistoryEntry.SlidePackFK = ModifiedSlidePack
                NewVersionHistoryEntry.ModDate = timezone.now()
                NewVersionHistoryEntry.save()
        return redirect('ModuleBoardTutor', req_Module_Code)
    return render(request, 'LectureBoard/LectureDayEdit.html', context)


@user_passes_test(check_Tutor_Group)
def New_LectureDay(request, req_Module_Code):
    '''Allows a Lecturer to be able to create a new Lecture Day for a given module'''
    ModuleInfo = get_object_or_404(Module, Module_Code=req_Module_Code)  # Getting information about the lecture day using the ID from URL
    current_date = timezone.now()  # Getting current time/date
    if request.method == "POST":
        LDform = LectureDayForm(request.POST, request.FILES)
        SPForm = SlidePackForm(request.POST, request.FILES)
        VHForm = VersionHistoryForm(request.POST, request.FILES)
        context = {
            'LDForm': LDform,
            'SPForm': SPForm,
            'VHForm': VHForm,
            'current_date': current_date,
        }
        LD_Creation = False
        
        if LDform.is_valid():
            NewLectureDay = LDform.save(commit=False)
            NewLectureDay.ModuleLectureBoard = ModuleInfo
            NewLectureDay.save()
            LD_Creation = True
            if SPForm.is_valid():
                NewSlidePack = SPForm.save(commit=False)
                NewSlidePack.LectureDay_FK = NewLectureDay
                NewSlidePack.save()
                slidepack = SlidePack.objects.get(LectureDay_FK=NewLectureDay)
                online_file = PPT_Convert.detect_file_type(PPT_Convert(), slidepack.OriginalFile.path)
                slidepack.OnlineSlidePack.name = online_file
                slidepack.save()
                if VHForm.is_valid():
                    NewVersionHistoryEntry = VHForm.save(commit=False)
                    NewVersionHistoryEntry.SlidePackFK = NewSlidePack
                    NewVersionHistoryEntry.ModDate = timezone.now()
                    NewVersionHistoryEntry.save()
        if LD_Creation:
            return redirect('ModuleBoardTutor', req_Module_Code)
    else:
        LDform = LectureDayForm()
        SPForm = SlidePackForm()
        VHForm = VersionHistoryForm()
        context = {
            'LDForm': LDform,
            'SPForm': SPForm,
            'VHForm': VHForm,
            'current_date': current_date,
        }
    return render(request, 'LectureBoard/LectureDayNew.html', context)

@user_passes_test(check_Tutor_Group)
def Delete_LectureDay(request, req_Module_Code, lecture_id):
    query = LectureDay.objects.get(id=lecture_id)
    try:
        slidepackQuery = SlidePack.objects.get(LectureDay_FK=query)
        os.remove(slidepackQuery.OriginalFile.path)
        os.remove(slidepackQuery.OnlineSlidePack.path)
    except Exception as e:
        print('Error occurred:', e)
        pass
    query.delete()
    return redirect('ModuleBoardTutor', req_Module_Code)

@login_required
def LectureBoardSearch(request):
    '''Allows a user to be able to use a search term and returns a list of possible results'''
    if request.method == "POST":
        searched = request.POST['searched']
        lecturedays = LectureDay.objects.filter(Q(Title__contains=searched) | Q(Description__contains=searched) | Q(Date__contains=searched))
        count = lecturedays.count()
        context = {
            'searched': searched,
            'lecturedays': lecturedays,
            'num_results': count,
        }
        return render(request, 'LectureBoard/Search.html', context)
    else:
        return render(request, 'LectureBoard/Search.html')

