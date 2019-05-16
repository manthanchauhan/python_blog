from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountTests(TestCase):

    def test_login_status_code(self):
        url = reverse('login_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'login view fails')

    def test_login(self):
        self.user = User.objects.create_user(username='test',
                                             password='password',
                                             )
        url = reverse('login_url')
        response = self.client.post(url, {'username': 'test',
                                          'password': 'password'},
                                    follow=True)
        self.assertEqual(response.context['user'].is_active, True, f'login not working {response}')

    def test_logout(self):
        url = reverse('logout_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.context['user'].is_active, False, f'logout is not working')

    def test_signup(self):
        details = {'username': 'test',
                   'email': 'abc@gmail.com',
                   'password1': 'eB8afdfsfs',
                   'password2': 'eB8afdfsfs',
                   }
        url = reverse('signup_url')
        response = self.client.post(url, details, follow=True)
        self.assertEqual(response.context['user'].is_active, True, f'signup is not working')


class PasswordResetTests(TestCase):
    def setup(self):
        url = reverse('password_reset_url')
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200, f'status code error in password reset')
