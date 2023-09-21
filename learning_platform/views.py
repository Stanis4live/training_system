from rest_framework import viewsets
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated


# API для выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ, с выведением информации
# о статусе и времени просмотра
class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        # Получаем доступы к продуктам для пользователя.
        product_accesses = user.product_accesses.all()
        # Возвращаем список уникальных уроков (Lesson), которые связаны с продуктами из списка product_accesses
        return Lesson.objects.filter(products__in=product_accesses.values_list('product', flat=True)).distinct()

