from django.urls import path

from . import views

urlpatterns = [
    # Example: /LectureBoard/, this is for choosing a module but shows all modules
    path('', views.LectureBoardView, name='LectureBoard'), 
    # Example: /LectureBoard/WM393/, this is for viewing an individual Module
    path('<str:req_Module_Code>/', views.ModuleBoardView, name='ModuleBoard'),
    # Example: /LectureBoard/WM393/1, this is for viewing an invidual lecture day
    path('<str:req_Module_Code>/<int:lecture_id>/', views.LectureDayView, name='LectureDay')

    # ADMIN:
    # Example: LectureBoard/Tutor/, this is where a lecturer can view/edit/delete all their modules
    path('', views.LectureBoardView, name='LectureBoardTutor'), 
    # Example: LectureBoard/Tutor/WM393/, this is to view/edit/delete an invidual Module Board
    path('Tutor/<str:req_Module_Code>/', views.ModuleBoardView, name='ModuleBoardTutor'),
    # Example: LectureBoard/Tutor/WM393/1, this is to view/edit/delete an invidual lecture day
    path('Tutor/<str:req_Module_Code>/<int:lecture_id>/', views.LectureDayView, name='LectureDayTutor')

]
