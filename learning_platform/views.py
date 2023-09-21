from django.contrib.auth.models import User
from django.db.models import Prefetch, Count, Sum, F
from rest_framework import viewsets
from .models import Lesson, Product, LessonViewing
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
        lesson_viewings_for_user = LessonViewing.objects.filter(user=user)
        return (Lesson.objects.filter(products__in=product_accesses.values_list('product', flat=True))
                .prefetch_related(Prefetch('user_viewings', queryset=lesson_viewings_for_user))
                .distinct())


class ProductLessonsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = ProductLessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        if not user.product_accesses.filter(product_id=product_id).exists():
            raise PermissionDenied("У вас нет доступа к этому продукту.")

        lesson_viewings_for_user = LessonViewing.objects.filter(user=user).order_by('-updated_at')
        return (Lesson.objects.filter(products__id=product_id)
                .prefetch_related(Prefetch('user_viewings', queryset=lesson_viewings_for_user)))


class ProductStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStatisticsSerializer

    def get_queryset(self):
        total_users = User.objects.count()
        annotated_queryset = Product.objects.annotate(
            total_lessons_viewed=Count('lessons__user_viewings'),
            total_time_spent=Sum('lessons__user_viewings__viewed_duration'),
            total_students=Count('user_accesses'),
            purchase_percentage=F('user_accesses') / total_users * 100
        )
        return annotated_queryset


