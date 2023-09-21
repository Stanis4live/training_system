from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, ProductLessonsViewSet, ProductStatisticsViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet)
router.register(r'products/(?P<product_id>\d+)/lessons', ProductLessonsViewSet, basename='product-lessons')
router.register(r'product-statistics', ProductStatisticsViewSet, basename='product-statistics')


urlpatterns = [
    path('', include(router.urls)),
]
