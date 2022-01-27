from django.urls import reverse
from django.test import TestCase, Client

# Creating Client object:
client = Client()


class ModuleOverviewViewTests(TestCase):
    
    def tbc_test_no_modules(self):
        '''
        If no modules exist, an appropriate message is displayed.
        '''
        response = self.client.get(reverse('LectureBoard:Overview_StudentModules'))  # There is an issue with the namespace in reverse
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have not been enrolled into any modules yet, please contact your Apprentice Tutor for support on this :(')
        self.assertQuerysetEqual(response.context['ModulesEnrolled', []])


