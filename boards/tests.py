from django.test import TestCase
from django.urls import reverse
from articles.models import Article
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class ViewTests(TestCase):
    def setUp(self):
        art = Article.objects.create(title='test',
                                     description='test',
                                     content='tests/content.html',
                                     thumbnail='tests/thumbnail.jpeg'
                                     )
        self.board = models.Board.objects.create(article=art)

        self.user = User.objects.create_user(username='test_user',
                                             password='fdklafdsfsdf')

    def test_all_boards_view_status_code(self):
        url = reverse('boards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'all boards list view failed')

    def test_board_view_redirection(self):
        url = reverse('board_url', kwargs={'id_': self.board.id})
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login_url")}?next={url}', status_code=302)

    def test_board_view_status_code(self):
        self.client.login(username='test_user', password='fdklafdsfsdf')
        url = reverse('board_url', kwargs={'id_': self.board.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'board_view failed')

    def test_board_commenting(self):
        url = reverse('board_url', kwargs={'id_': self.board.id})
        self.client.post(url, {'query': 'test_comment'})
        self.assertEqual(len(self.board.posts.all()), 1, f'post creation fails')

    def test_post_reply_redirection(self):
        post = models.Post.objects.create(content='hi',
                                          board=self.board,
                                          )

        url = reverse('reply_url', kwargs={'id_': post.id})
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login_url")}?next={url}', status_code=302)

    def test_post_reply_status_code(self):
        post = models.Post.objects.create(content='hi',
                                          board=self.board,
                                          )

        self.client.login(username='test_user', password='fdklafdsfsdf')
        url = reverse('reply_url', kwargs={'id_': post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'reply_view failed')



