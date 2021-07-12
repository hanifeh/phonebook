from django.contrib.auth import get_user_model
from django.test import TestCase
from . import models
from django.test import Client

# Create your tests here.
from django.urls import reverse


class PhoneBookTestCase(TestCase):
    """
        test phonebook
    """

    def testUp(self):
        self.client = Client()

    def test_creat_auth_required(self):
        """
        Tests if view redirects anonymous user to login page
        """
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        response = self.client.get(reverse('create'), follow=True)
        self.assertContains(response, 'Login')

    def test_create_view_with_login_user(self):
        """
        A new user should see create page
        """
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('create'))
        self.assertContains(response, 'First name:')
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123456789'}
                                    )

        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123456789'})

        self.assertEqual(response.status_code, 422)

    def test_invalid_date_for_create(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123456789'})

        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123789'})

        self.assertEqual(response.status_code, 400)

    def test_uniq_together(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123456789'})

        self.assertEqual(response.status_code, 200)
        user2 = get_user_model().objects.create(username='user2')
        self.client.force_login(user=user2)
        response = self.client.post(reverse('create'), {'first_name': 'testfirst',
                                                        'last_name': 'testlast',
                                                        'phone_number': '09123456789'})

        self.assertEqual(response.status_code, 200)

    def test_search_login_required(self):
        response = self.client.get(reverse('new search'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        response = self.client.get(reverse('new search'), follow=True)
        self.assertContains(response, 'Login')

    def test_search_with_login_user(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        models.MyUser.objects.create(first_name='test', last_name='test', phone_number='09123456789', user=user)
        response = self.client.get(reverse('new search'), {'searched': '0912', 'mode': '1'})
        self.assertEqual(response.context_data['paginator'].count, 1)
        response = self.client.get(reverse('new search'))
        self.assertEqual(response.context_data['paginator'].count, 1)
        response = self.client.get(reverse('new search'), {'searched': '0912', 'mode': '2'})
        self.assertEqual(response.context_data['paginator'].count, 0)

    def test_phonebook_login_required(self):
        response = self.client.get(reverse('phonebook'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        response = self.client.get(reverse('phonebook'), follow=True)
        self.assertContains(response, 'Login')

    def test_phonebook_with_login_user(self):
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        models.MyUser.objects.create(first_name='test', last_name='test', phone_number='09123456789', user=user, pk=1)
        response = self.client.get(reverse('phonebook'))
        self.assertEqual(response.context_data['paginator'].count, 1)
        response = self.client.get('/editnumber/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/editnumber/1', {'first_name': 'testfirst',
                                                      'last_name': 'testlast',
                                                      'phone_number': '09123456'})
        self.assertContains(response, 'phone number invalid')
        response = self.client.post('/editnumber/1', {'first_name': 'testfirst',
                                                      'last_name': 'testlast',
                                                      'phone_number': '09123456788'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_action_login_required(self):
        response = self.client.get(reverse('action'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        response = self.client.get(reverse('action'), follow=True)
        self.assertContains(response, 'Login')