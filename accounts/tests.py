from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.core import mail


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200,
                         f'password reset view failed')

    def test_view_function(self):
        view = resolve('/password_reset/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test_email@django.com',
                                             password='dasfsdfsdf')

    def test_redirection(self):
        url = reverse('password_reset')
        response = self.client.post(url, {'email': 'testemail@django.com'})
        url = reverse('password_reset_done')
        self.assertRedirects(response, url)

    def test_view_function(self):
        view = resolve(reverse('password_reset_done'))
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)


class ResetEmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test_email@django.com',
                                             password='dasfsdfsdf')
        mail.outbox = []
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': self.user.email})
        self.email = mail.outbox[0]

    def test_email_send(self):
        self.assertEqual(len(mail.outbox), 1, f'email not sent to valid id')

    def test_invalid_email_send(self):
        mail.outbox = []
        url = reverse('password_reset')
        self.client.post(url, {'email': 'random_email@django.com'})
        self.assertEqual(len(mail.outbox), 0, f'email sent to invalid id')

    def test_email_to(self):
        self.assertEqual(self.email.to, [self.user.email])

    def test_email_body(self):
        context = self.response.context
        token = context['token']
        uid = context['uid']

        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token,
        })
        self.assertIn(password_reset_token_url, self.email.body)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test_email@django.com',
                                             password='sfafsfsdfsdfsdf')

        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        self.uid = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(self.user)

        self.url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid,
                                                             'token': self.token})
        self.response = self.client.get(self.url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200, f'password reset confirm view fails')

    def test_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_invalid_token_url(self):
        # invalidated the url by changing user information
        self.user.password = 'sfdfsfsdfsdad'

        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.context[-1].get("title"), 'Password reset unsuccessful')


class PasswordResetCompeteTests(TestCase):
    def test_status_code(self):
        url = reverse('password_reset_complete')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'password reset '
        f'complete view failed')

    def test_view(self):
        view = resolve(reverse('password_reset_complete'))
        self.assertEqual(view.func.view_class, auth_views.PasswordResetCompleteView,
                         f'password reset complete view is changed')


class AccountTests(TestCase):

    def test_password_reset_done(self):
        url = reverse('password_reset')
        response = self.client.post(url, {'email': 'test_@gmail.com'})
        self.assertEqual(response.status_code, 302, f'reset done fails')

    def test_logout_status_code(self):
        url = reverse('logout_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'logout failed')

    def test_login_status_code(self):
        url = reverse('login_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'login view fails')

    def test_login_and_logout(self):
        self.user = User.objects.create_user(username='test',
                                             password='password',
                                             )
        url = reverse('login_url')
        response = self.client.post(url, {'username': 'test',
                                          'password': 'password'},
                                    follow=True)
        self.assertEqual(response.context['user'].is_active, True, f'login not working {response}')

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
