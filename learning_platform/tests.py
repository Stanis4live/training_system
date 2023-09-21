from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Product, Lesson, ProductAccess, LessonViewing


class LessonViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(title='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', video_link='https://example.com', duration=100)
        self.lesson.products.add(self.product)
        ProductAccess.objects.create(user=self.user, product=self.product)
        self.url = reverse('lesson-list')  # используйте соответствующее имя, если у вас другое

    def test_lesson_view_set(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProductLessonsViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(title='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', video_link='https://example.com', duration=100)
        self.lesson.products.add(self.product)
        self.url = reverse('product-lessons-list', args=[self.product.id])

    def test_product_lessons_view_set_without_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_lessons_view_set_with_access(self):
        ProductAccess.objects.create(user=self.user, product=self.product)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProductStatisticsViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(title='Test Product', owner=self.user)
        self.url = reverse('product-statistics-list')

    def test_product_statistics_view_set(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('title', response.data[0])
        self.assertIn('total_lessons_viewed', response.data[0])
        self.assertIn('total_time_spent', response.data[0])
        self.assertIn('total_students', response.data[0])
        self.assertIn('purchase_percentage', response.data[0])
