from django.test import TestCase
from django.urls import reverse
from articles.models import Article
from . import models


class ViewTests(TestCase):
    def test_board_view_status_code(self):
        art = Article.objects.create(title='test',
                                     description='test',
                                     content='tests/content.html',
                                     thumbnail='tests/thumbnail.jpeg'
                                     )
        brd = models.Board.objects.create(article=art)
        url = reverse('board_url', kwargs={'id_': brd.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'board_view failed')
