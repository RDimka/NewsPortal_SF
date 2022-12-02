from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum
from django.urls import reverse

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    date_time_in = models.DateTimeField(auto_now_add=True)
    is_news = models.BooleanField(default=True)  # True - новость, False - статья
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):  #увеличивают рейтинг на единицу
        self.rating = self.rating + 1
        self.save()

    def dislike(self):  #уменьшает рейтинг на единицу
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    # def __str__(self):
    #     return f'{self.title()}: {self.text[:20]}'
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    date_time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):  #увеличивают рейтинг на единицу
        self.rating = self.rating + 1
        self.save()

    def dislike(self):  #уменьшает рейтинг на единицу
        self.rating = self.rating - 1
        self.save()


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # обновляет рейтинг пользователя, переданный в аргумент этого метода.
    # Он состоит из следующего:
    # суммарный рейтинг каждой статьи автора умножается на 3;
    # суммарный рейтинг всех комментариев автора;
    # суммарный рейтинг всех комментариев к статьям автора.
    def update_rating(self):
        post_ratings = 0
        comment_ratings = 0
        post_comment_ratings = 0
        #получить рейтинги ТОЛЬКО статей конкретного автора, просуммировать, *3
        if self.post_set.filter(is_news=False).exists():  #проверка есть ли у автора статьи
            post_ratings = self.post_set.filter(is_news=False).aggregate(Sum('rating'))['rating__sum']*3

            #получить рейтинги всех комментариев автора
        if self.user.comment_set.all().exists():  #проверка есть ли комментарии от данного автора
            comment_ratings = self.user.comment_set.all().aggregate(Sum('rating'))['rating__sum']

             #получить рейтинги всех комментариев к статьям автора
        if self.post_set.all().exists():  #проверка есть ли комментарии к статьям автора
            post_comment_ratings = self.post_set.all().aggregate(Sum('comment__rating'))['comment__rating__sum']

        self.rating = post_ratings + comment_ratings + post_comment_ratings
        self.save()

        return self.rating

