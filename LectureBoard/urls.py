from django.urls import path

from . import views

urlpatterns = [
    # VIEW ONLY Views:

    # Example: /LectureBoard/, this is for choosing a module but shows all modules
    path('', views.Overview_StudentModules, name='Overview'), 
    # Example: /LectureBoard/WM393/, this is for viewing an individual Module
    path('<str:req_Module_Code>/', views.ModuleBoard_StudentView, name='ModuleBoard'),
    # Example: /LectureBoard/WM393/1, this is for viewing an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/', views.LectureDay_StudentView, name='LectureDay'),
    # Example: /LectureBoard/search/SearchTerm/
    path('search', views.LectureBoardSearch, name="LectureBoardSearch"),

    # EDITING Views:

    # Example: LectureBoard/Modules/edit/, this is where a Lecturer can view/edit/delete all of their modules
    path('Modules/edit/', views.Overview_Tutor, name='Overview_Tutor'),
    # Example: LectureBoard/Tutor/WM393/edit/, this is to view/delete an invidual Module Board
    path('<str:req_Module_Code>/edit/', views.ModuleBoardTutor, name='ModuleBoardTutor'),

    # Module Editing:

    # Example: LectureBoard/Modules/new/edit/, this is where a lecturer can view/edit/delete all their modules
    path('Modules/new/edit/', views.New_Module, name='New_Module'), 
    # Example: LectureBoard/Modules/WM393/edit/, this is where a lecturer can view/edit/delete all their modules
    path('Modules/<str:req_Module_Code>/edit/', views.Edit_Module, name='Edit_Module'), 
    # Example: LectureBoard/Modules/WM393/delete/, this is where a lecturer can view/edit/delete all their modules
    path('Modules/<str:req_Module_Code>/delete/', views.Delete_Module, name='Delete_Module'), 

    # Lecture Day Editing:
     
    # Example: LectureBoard/Tutor/WM393/New/edit/, this is to create an invidual lecture day
    path('<str:req_Module_Code>/New/edit/', views.New_LectureDay, name='New_LectureDay'),
    # Example: LectureBoard/Tutor/WM393/1/edit/, this is to edit an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/edit/', views.Edit_LectureDay, name='Edit_LectureDay'),
    # Example: LectureBoard/Tutor/WM393/1/delete/, this is to delete an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/delete/', views.Delete_LectureDay, name='Delete_LectureDay'),

]


