from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='tags_created')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True)
    content = models.FileField(upload_to='uploaded_articles/', unique=True)
    thumbnail = models.ImageField(upload_to='uploaded_articles/')

    # if user is deleted author will be set as null
    # rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)],
    #                              default=5)
    authors = models.ManyToManyField(User, related_name='articles_written')
    tags = models.ManyToManyField(Tag, related_name='articles_tagged')
    date_created = models.DateTimeField(auto_now_add=True,
                                        db_column='data_created')

    def __str__(self):
        return self.title
