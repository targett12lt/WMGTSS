import os

# Importing objects from other modules:
from .models import Module, ModuleAccess, LectureDay, SlidePack, VersionHistory
from .forms import ModuleForm, LectureDayForm, SlidePackForm, VersionHistoryForm
from .processing import PPT_Convert

# Importing required django modules:
from django.http import Http404
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.models import Group


def check_Tutor_Group(user):
    '''Checks if a user is in the "Tutors" permission group'''
    if user:
        return user.groups.filter(name='Tutors').exists()
    return False

def get_subscribed_modules(request):
    '''Gets a list of the subscribed modules for a given user, requires "request" as parameter'''
    list_of_users_groups = list(request.user.groups.values_list('name', flat=True))
    Permission_To_Access = list(ModuleAccess.objects.filter(UserGroupName__in=list_of_users_groups).values_list('Module_Identifier', flat=True))
    return Permission_To_Access

# Student Views:

@login_required  # ensuring only logged in users can access page
def Overview_StudentModules(request):
    '''Shows a Student all the Modules that they are subscirbed to'''
    Permission_To_Access = get_subscribed_modules(request)
    ModulesEnrolled = Module.objects.filter(id__in=Permission_To_Access)
    context = {
        'SearchFunctionality': True,  # Make search functionality visible
        'ModulesEnrolled': ModulesEnrolled  # List of students modules
    }
    return render(request, 'LectureBoard/Overview.html', context)


@login_required
def ModuleBoard_StudentView(request, req_Module_Code):
    '''
    Student view for a Module that they are subscribed to - requires the ModuleCode
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    '''
    try:
        Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)  # Getting list of lectures
        context = {
            'SearchFunctionality': True,
            'LectureList': LectureList,
            'Module_Info': Module_Info}  # passing required data to HTML Template
    except Module.DoesNotExist:
        raise Http404('The module requested: "' + req_Module_Code + '" does not exist.'
        '\n\nPlease contact your system administrator for further support.\n\n')
    
    return render(request, 'LectureBoard/ModuleBoard.html', context)


@login_required
def LectureDay_StudentView(request, req_Module_Code,lecture_id):
    '''Provides a view for each lecture day, allowing user to see SlidePack, 
    and Version History objects.

    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    * lecture_id = Auto-incrementing integer ID, PK for the lecture days, used to locate the lecture day and slidepack info
    '''

    # Checking if LectureDay exists and getting data:
    LectureDayInfo = get_object_or_404(LectureDay, id=lecture_id)  # Getting information about the lecture day using the ID from URL
    Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
    Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
    Version_History = None

    try:
        RelatedLDs = LectureDay.objects.filter(Q(ModuleLectureBoard = Module_PK) & ~Q(id=lecture_id))[:2]
        SlidePackInfo = SlidePack.objects.get(LectureDay_FK = lecture_id)
    except Exception:
        pass  # If no slidepack associated   

    # Trying to check if it has any version history:
    try:
        Version_History = VersionHistory.objects.filter(SlidePackFK = SlidePackInfo)
    except Exception as e:
        pass 

    # Packaging all data from DB into context to load into HTML template:
    context = {
        'SearchFunctionality': True,
        'LectureDayInfo': LectureDayInfo,
        'SlidePackInfo': SlidePackInfo,
        'RelatedLDs': RelatedLDs,
        'Module_Info': Module_Info,
        'Version_History': Version_History,
        }
    return render(request, 'LectureBoard/LectureDay.html', context)


# Tutor/edit views:

# --- Module Management (multiple) ---
@user_passes_test(check_Tutor_Group)
def Overview_Tutor(request):
    '''Allows a Tutor to view the Modules that they own and are subscribed to'''

    Permission_To_Access = get_subscribed_modules(request)  # Checking what they have permission to access
    ModulesEnrolled = Module.objects.filter(id__in=Permission_To_Access)  # Showing only modules they are subscribed to
    ModulesOwned = Module.objects.filter(Module_Tutor=request.user)  # Shows only modules that they own
    context = {
        'SearchFunctionality':True,
        'ModulesEnrolled':ModulesEnrolled,
        'ModulesOwned': ModulesOwned,
    }
    return render(request, 'LectureBoard/OverviewTutor.html', context)


@user_passes_test(check_Tutor_Group)
def New_Module(request):
    '''Allows a Tutor to be able to add a new module to the Database using 
    Django form'''

    permission_groups = Group.objects.all()  # Getting a list of all permission groups
    if request.method == "POST":  # Getting data using POST
        form = ModuleForm(request.POST)
        if form.is_valid():
            NewModule = form.save(commit=False)
            NewModule.Module_Tutor = request.user
            NewModule.save()
            checked_items = request.POST.getlist("item_checkbox")
            for i in checked_items:
                ModuleAccess.objects.create(Module_Identifier = NewModule, UserGroupName=i)
            return redirect('Overview_Tutor')  # Redirecting user if form is vaild
    else:
        form = ModuleForm()
    return render(request, 'LectureBoard/Overview_NewModule.html', {'form': form, 'permission_groups': permission_groups})


@user_passes_test(check_Tutor_Group)
def Edit_Module(request, req_Module_Code):
    '''
    Allows a Lecturer to modify an exising Module
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    '''
    permission_groups = Group.objects.all()  # Getting list of all permission groups
    permission_groups_names = list(permission_groups.values_list('name', flat=True))
    ModuleInstance = Module.objects.get(Module_Code = req_Module_Code)  # getting instance of module to be modified
    permission_groups_access = list(ModuleAccess.objects.filter(Module_Identifier=ModuleInstance).values_list('UserGroupName', flat=True))
    bools = []  # creating list of bools, showing what groups have permission to module
    for i in permission_groups_names:
        if i in permission_groups_access:
            bools.append("checked")
        else:
            bools.append("")
    form = ModuleForm(request.POST or None, instance=ModuleInstance)  # Passing instance to form
    if form.is_valid():  # Checking if form is vaild
        EditModule = form.save(commit=False)
        EditModule.Module_Tutor = request.user
        EditModule.save()  # Saving Chances to Module item
        query = ModuleAccess.objects.filter(Module_Identifier = EditModule)
        query.delete()  # Deleting previous Module Access
        checked_items = request.POST.getlist("item_checkbox")
        for i in checked_items:
            ModuleAccess.objects.create(Module_Identifier = EditModule, UserGroupName=i)  # Updating permission to Module
        return redirect('Overview_Tutor')

    return render(request, 'LectureBoard/Overview_EditModule.html', {'form': form, 'permission_groups': zip(permission_groups, bools)})


def Delete_Module(request, req_Module_Code):
    '''Deletes a module and redirects the Tutor to their Overview page'''
    query = Module.objects.get(Module_Code=req_Module_Code)
    query.delete()
    return redirect('Overview_Tutor')


# --- Individual Module Management --- 


@user_passes_test(check_Tutor_Group)
def ModuleBoardTutor(request, req_Module_Code):
    '''
    Allows a Tutor to be able to view and modify information about a given Module
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    '''
    try:
        Module_Info = Module.objects.get(Module_Code = req_Module_Code)  # Checking module exists
        Module_PK = list(Module.objects.filter(Module_Code = req_Module_Code).values_list('id', flat=True))[0]
        LectureList = LectureDay.objects.filter(ModuleLectureBoard = Module_PK)  # Getting LD objecs
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
    '''
    Allows a Tutor to modify an existing LectureDay and the associated SlidePack and VersionHistory    
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    * lecture_id = Auto-incrementing integer ID, PK for the lecture days, used to locate the lecture day and slidepack info
    '''
    LDInstance = get_object_or_404(LectureDay, pk=lecture_id)
    SPInstance = get_object_or_404(SlidePack, LectureDay_FK=LDInstance)
    Previous_Version_History = None
    
    # Getting the original SP file path, so can be compared with new one: 
    try:
        OriginalSP = SPInstance.OriginalFile.path
        OriginalOnlineSP = SPInstance.OnlineSlidePack.path
    except Exception:  # If SlidePack wasn't added or PDF conversion failed
        pass

        # Trying to check if it has any version history
    try:
        Previous_Version_History = VersionHistory.objects.filter(SlidePackFK = SPInstance)
    except Exception as e:
        pass
    
    # Created Forms required for View:
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
    # Checking forms are vaild and creating new SlidePack objects:
    if LDForm.is_valid():
        ModifiedLectureDay = LDForm.save(commit=False)
        ModifiedLectureDay.save()
        if SPForm.is_valid():
            ModifiedSlidePack = SPForm.save(commit=False)
            ModifiedSlidePack.save()  # Saving updated SlidePack object
            slidepack = SlidePack.objects.get(LectureDay_FK=ModifiedLectureDay)
            ModifiedSP = slidepack.OriginalFile.path
            # Checking if slidepack has been changed:
            if ModifiedSP != OriginalSP:
                try:
                    os.remove(OriginalSP)  # Removing original SlidePack
                    os.remove(OriginalOnlineSP)  # Removing original online SlidePack
                    online_file = PPT_Convert.detect_file_type(PPT_Convert(), slidepack.OriginalFile.path)
                    slidepack.OnlineSlidePack.name = online_file
                    slidepack.save()  # Saving SlidePack object with new online Slide Pack PDF File
                except Exception:  # Passes os.remove if files do not exist
                    pass
            if VHForm.is_valid():
                NewVersionHistoryEntry = VHForm.save(commit=False)
                NewVersionHistoryEntry.SlidePackFK = ModifiedSlidePack
                NewVersionHistoryEntry.ModDate = timezone.now()
                NewVersionHistoryEntry.save()
        return redirect('ModuleBoardTutor', req_Module_Code)

    return render(request, 'LectureBoard/LectureDayEdit.html', context)


@user_passes_test(check_Tutor_Group)
def New_LectureDay(request, req_Module_Code):
    '''
    Allows a Lecturer to be able to create a new Lecture Day and the associated SlidePack and VersionHistory    
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    '''
    ModuleInfo = get_object_or_404(Module, Module_Code=req_Module_Code)  # Getting information about the lecture day using the ID from URL
    current_date = timezone.now()  # Getting current time/date
    if request.method == "POST":
        # Creating required form objects and calling request.POST and reequest.FILES
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
            return redirect('ModuleBoardTutor', req_Module_Code)  # redirect if form not vaild
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
    '''
    Allows a Tutor to delete a LectureDay and associated objects
    
    Parameters:
    * request - django HTTP request framework requirement
    * req_Module_Code - This is the University Academic Module (i.e. WM393).
    * lecture_id = Auto-incrementing integer ID, PK for the lecture days, used to locate the lecture day and slidepack info
    '''
    query = LectureDay.objects.get(id=lecture_id)  # Getting LD object
    try:
        slidepackQuery = SlidePack.objects.get(LectureDay_FK=query)
        os.remove(slidepackQuery.OriginalFile.path)  # Removing PPT file
        os.remove(slidepackQuery.OnlineSlidePack.path)  # Removing PDF file
    except Exception as e:
        pass
    query.delete()  # Delting LD object from DB
    return redirect('ModuleBoardTutor', req_Module_Code)  # Redirect Tutor to their Module Board


@login_required
def LectureBoardSearch(request):
    '''Allows a user to be able to use a search term and returns a list of possible results'''
    if request.method == "POST":  # Checking request method is 'POST'
        searched = request.POST['searched']  # Grabbing search term
        lecturedays = LectureDay.objects.filter(Q(Title__contains=searched) | Q(Description__contains=searched) | Q(Date__contains=searched))
        count = lecturedays.count()  # Counting number of search results found matching query
        context = {
            'searched': searched,
            'lecturedays': lecturedays,
            'num_results': count,
        }
        return render(request, 'LectureBoard/Search.html', context)  # Returns search results page populated with results
    else:
        return render(request, 'LectureBoard/Search.html')  # Returns blank search results if no search term inputted

