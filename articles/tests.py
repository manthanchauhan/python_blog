from django.test import TestCase
from django.urls import reverse
from . import models
import mock

class HomeTests(TestCase):
    def test_home_status_code(self):
        url = reverse('home_url')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'home view fails')

    def test_articles_status_code(self):
        url = reverse('modify_articles_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'articles view fails')

    def test_article_view_status_code(self):

        self.assertEqual(len(models.Article.objects.all()), 0)
        # article_ = models.Article.objects.all()[0]
        # url = reverse('article_url', kwargs={'id_': article_.id})
        # url = 'http://127.0.0.1:8000/articles/4/'
        # response = self.client.get(url, follow=True)
        # self.assertEqual(response.status_code, 200, f' view failed')