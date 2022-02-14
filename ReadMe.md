# WMGTSS LectureBoard

## About The Project
WMGTSS is a cross-functional system that has been designed to support WMG students and tutors by providing the functionality required in a  post-pandemic environment.  This report focuses on the requirements, architecture and development of the core WMGTSS system functionality and one  board specifically: the Lecture Board. It has been assumed when designing this system, that Warwick University’s SSL service is not available, hence  requiring user identification and authentication functionality to also be required. The Lecture Board must allow users to access content for any  given lecture day, navigate through the slide pack, in addition to allowing the user to store it locally. 

This project has been built using Python 3 and BootStrap 4. All external modules and dependencies are listed below and a set-up guide is also available in this ReadMe file.  

## Built With: 
* Python 3.7.6 
* Django 3.2.8 - Requires Installation  
* django-crispy-forms 1.14.0 - Requires Installation  
* pathlib - Requires Installation  
* pywin32 303 - Requires Installation  
* comtypes 1.1.7 - Required Installation  
* mock 4.03 - Requires Installation  
* os  
* datetime  
* sys  
* BootStrap 4.5.2

### Prerequisites:
* All libraries previously listed are installed on your machine - use 'pip' install to install libraries as required.  
* Project must be ran on a Windows machine with Microsoft PowerPoint installed, to allow the PPT/PPTX -> PDF conversion to work.  
* Machine MUST have a connection to the internet (to access BootStrap JS).

### Set-Up
1. Source Code can be downloaded from the Source Code submission on Tabula or cloned from the Source Code Version Control Repository:
`git clone https://github.com/targett12lt/WMGTSS.git`  
It is recommended to used the Source Code submmited to Tabula, as this also includes some sample data and files to test the functionality of the system.  
2. Launch Project Folder and Run in local IDE (e.g. Microsoft Visual Studio Code)  
3. Launch 'Windows Powershell' Terminal Window in IDE  
4. Set Working Directiory of Terminal to 'WMGTSS'
5. Run the following command: 
`python manage.py runserver`  
This will start a development server on your local machine, a message will be returned containing the address for the local server. This was:  
`http://127.0.0.1:8000/`

## GIT
To download the latest release of this source code please visit:  
https://github.com/targett12lt/WMGTSS
