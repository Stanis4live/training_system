from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    video_link = models.URLField()
    duration = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, related_name='lessons')

    def __str__(self):
        return self.title


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_accesses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_accesses')


class LessonViewing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_viewings')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_viewings')
    viewed_duration = models.PositiveIntegerField()

    @property
    def status(self):
        if self.viewed_duration >= self.lesson.duration * 0.8:
            return "Просмотрено"
        return "Не просмотрено"