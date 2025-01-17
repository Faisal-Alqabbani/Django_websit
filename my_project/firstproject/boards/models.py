from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
from django.conf import settings
from django.urls import reverse
import math
class Board(models.Model):
    name = models.CharField(max_length=20,unique=True)
    description = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True)
    #return object as string in database
    def __str__(self):
        return self.name
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_dt').first()
class Topic(models.Model):
    subject = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    board = models.ForeignKey(Board,related_name='topics', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

class Post(models.Model):
    message = models.TextField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='post_like')
    created_by = models.ForeignKey(User,related_name='posts', on_delete =models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        return reverse("posts:like-toggl",  kwargs= self.pk )

# Create your models here.
