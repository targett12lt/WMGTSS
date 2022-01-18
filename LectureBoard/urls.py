from django.urls import path

from . import views

urlpatterns = [
    # Example: /LectureBoard/
    path('', views.LectureBoard, name='LectureBoard_YourModules'), 
    # Example: /LectureBoard/WM393/
    path('<str:Module_Code>/', views.ModuleBoard, name='ModuleBoard'),
    # Example: /LectureBoard/WM393/1
    path('<str:Module_Code>/<int:lecture_id>/', views.LectureDayView, name='LectureDay')
]
