from django.test import TestCase
from django.urls import reverse
from . import models
from . import forms
from django.contrib.auth.models import User
from django.conf import settings
import os


class HomeTests(TestCase):
    def test_home_status_code(self):
        url = reverse('home_url')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f'home view fails')

    def test_articles_status_code(self):
        url = reverse('modify_articles_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'articles view fails')

    def test_tags_status_code(self):
        url = reverse('modify_tags_url')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'tags view fails')


class ArticleTests(TestCase):
    @staticmethod
    def create_article():
        new_article = models.Article.objects.create(title='test_title',
                                                    description='test_article',
                                                    content='tests/content.html',
                                                    thumbnail='tests/thumbnail.jpeg',
                                                    )
        return new_article

    def test_article_view_status_code(self):
        new_article = self.create_article()
        url = reverse('article_url', kwargs={'id_': new_article.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f' view failed')


class TagTests(TestCase):
    @staticmethod
    def create_tag():
        tag = models.Tag.objects.create(title='test',
                                        description='test')
        return tag

    def test_tag_view_status_code(self):
        tag = self.create_tag()
        url = reverse('tag_url', kwargs={'id_': tag.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, f'tag view failed')
