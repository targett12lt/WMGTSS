from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

# Creating Client object:
client = Client()


class LectureBoardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dts_grp = Group.objects.get(name='Tutors')
        self.user = User.objects.create_user('test_user', 'test@user.com', 'test_password')
        self.dts_grp.user_set.add(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/LectureBoard/')
        self.assertEqual(response.status_code, 200)


