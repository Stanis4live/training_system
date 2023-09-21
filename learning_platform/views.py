from rest_framework import viewsets
from .models import Lesson, Product
from .serializers import LessonSerializer, ProductLessonSerializer, ProductStatisticsSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_accesses = user.product_accesses.all()
        return Lesson.objects.filter(products__in=product_accesses.values_list('product', flat=True)).distinct()


class ProductLessonsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = ProductLessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        if not user.product_accesses.filter(product_id=product_id).exists():
            raise PermissionDenied("У вас нет доступа к этому продукту.")

        return Lesson.objects.filter(products__id=product_id)


class ProductStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductStatisticsSerializer


