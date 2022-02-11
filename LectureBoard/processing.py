import win32com.client
import pythoncom
import os

class PPT_Convert():
    '''Class containing functions to detect and convert PowerPoint files to PDF'''
    
    def detect_file_type(self,file_name):
        '''Detects the file type and directs file to correct function to convert
        to PDF. Only accepts PPT or PPTX'''
        if file_name.endswith('.ppt'):
            file = self.ppt_to_pdf(file_name)
        elif file_name.endswith('.pptx'):
            file = self.pptx_to_pdf(file_name)
        else:
            file = ''
        return file
        
    def pptx_to_pdf(self, file_name):
        '''Converts PPTX files to PDF format. Keeps original file and makes PDF
        version in 'online' folder.'''
        try:
            filename_no_ext = os.path.basename(file_name[:-5])
            online_loc = os.path.join(os.getcwd(), r'media\\SlidePacks\\online\\', filename_no_ext)
            relative_file_loc_no_ext = os.path.join(r'SlidePacks\\online\\', filename_no_ext)
            relative_file_loc = (relative_file_loc_no_ext + '.pdf')
            powerpoint=win32com.client.Dispatch("Powerpoint.Application",pythoncom.CoInitialize())
            deck = powerpoint.Presentations.Open(file_name, WithWindow=False)
            deck.SaveAs(online_loc, 32) # formatType = 32 for ppt to pdf
            deck.Close()
            powerpoint.Quit()
            return relative_file_loc
        except:
            print("Could not open the file!")

    def ppt_to_pdf(self, file_name):
        '''Converts PPT to PDF format. Keeps original file and makes PDF version
        in 'online' folder.'''
        try:
            filename_no_ext = os.path.basename(file_name[:-4])
            online_loc = os.path.join(os.getcwd(), r'media\\SlidePacks\\online\\', filename_no_ext)
            relative_file_loc_no_ext = os.path.join(r'SlidePacks\\online\\', filename_no_ext)
            relative_file_loc = (relative_file_loc_no_ext + '.pdf')
            powerpoint=win32com.client.Dispatch("Powerpoint.Application",pythoncom.CoInitialize())
            deck = powerpoint.Presentations.Open(file_name, WithWindow=False)
            deck.SaveAs(online_loc, 32) # formatType = 32 for ppt to pdf
            deck.Close()
            powerpoint.Quit()
            return relative_file_loc
        except:
            print("Could not open the file!")

