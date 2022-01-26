from django.urls import path

from . import views

urlpatterns = [
    # Example: /LectureBoard/, this is for choosing a module but shows all modules
    path('', views.Overview_StudentModules, name='Overview'), 
    # Example: /LectureBoard/WM393/, this is for viewing an individual Module
    path('<str:req_Module_Code>/', views.ModuleBoard_StudentView, name='ModuleBoard_StudentView'),
    # Example: /LectureBoard/WM393/1, this is for viewing an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/', views.LectureDay_StudentView, name='LectureDay_StudentView'),

    # ADMIN:
    # Example: LectureBoard/Tutor/, this is where a lecturer can view/edit/delete all their modules
    path('Modules/edit/', views.Overview_EditModules, name='LectureBoard_Edit'), 
    # Example: LectureBoard/Tutor/WM393/, this is to view/edit/delete an invidual Module Board
    path('<str:req_Module_Code>/edit/', views.ModuleBoard_EditView, name='ModuleBoard_EditView'),
    # Example: LectureBoard/Tutor/WM393/1, this is to view/edit/delete an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/edit/', views.LectureDay_EditView, name='LectureDay_EditView'),

]
