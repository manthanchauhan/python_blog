from django.test import TestCase
from django.urls import reverse
from articles.models import Article
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class ViewTests(TestCase):
    @staticmethod
    def create_board():
        art = Article.objects.create(title='test',
                                     description='test',
                                     content='tests/content.html',
                                     thumbnail='tests/thumbnail.jpeg'
                                     )
        brd = models.Board.objects.create(article=art)
        return brd

    def test_board_view_status_code(self):
        brd = self.create_board()
        url = reverse('board_url', kwargs={'id_': brd.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'board_view failed')

    def test_signup_status_code(self):
        url = reverse('signup_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'signup view fails')

    def test_post_reply_status_code(self):
        brd = self.create_board()
        post = models.Post.objects.create(content='hi',
                                          board=brd,
                                          )
        url = reverse('reply_url', kwargs={'id_': post.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'reply_view failed')



