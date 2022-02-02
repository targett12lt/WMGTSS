import win32com.client
import os

class PPT_Convert():
    '''Class containing functions to detect and convert PowerPoint files to PDF'''
    root = os.path.dirname(os.path.abspath(__file__))

    def detect_file_type(self,file_name):
        '''Detects the file type and directs file to correct function to convert
        to PDF. Only accepts PPT or PPTX'''
        if file_name.endswith('.ppt'):
            self.ppt_to_pdf(file_name)
        elif file_name.endswith('.pptx'):
            self.pptx_to_pdf(file_name)
        else:
            print('incompatible file submitted')
        
    def pptx_to_pdf(self, file_name):
        '''Converts PPTX files to PDF format. Keeps original file and makes PDF
        version in 'online' folder.'''
        try:
            filename_no_ext = os.path.basename(file_name[:-5])
            online_loc = os.path.join(os.getcwd(), 'media\SlidePacks\online\\',
            filename_no_ext)
            powerpoint = win32com.client.Dispatch("Powerpoint.Application")
            deck = powerpoint.Presentations.Open(file_name, WithWindow=False)
            deck.SaveAs(online_loc, 32) # formatType = 32 for ppt to pdf
            deck.Close()
            powerpoint.Quit()
        except:
            print("Could not open the file!")

    def ppt_to_pdf(self, file_name):
        '''Converts PPT to PDF format. Keeps original file and makes PDF version
        in 'online' folder.'''
        try:
            filename_no_ext = os.path.basename(file_name[:-4])
            online_loc = os.path.join(os.getcwd(), 'media\SlidePacks\online\\',
            filename_no_ext)
            powerpoint = win32com.client.Dispatch("Powerpoint.Application")
            deck = powerpoint.Presentations.Open(file_name, WithWindow=False)
            deck.SaveAs(online_loc, 32) # formatType = 32 for ppt to pdf
            deck.Close()
            powerpoint.Quit()
            print('done')
        except:
            print("Could not open the file!")

