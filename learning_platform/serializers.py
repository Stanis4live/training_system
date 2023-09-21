from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Lesson, LessonViewing, Product


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'status', 'viewing_time']

    def get_status(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.status if viewing else "Не просмотрено"

    def get_viewing_time(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.viewed_duration if viewing else 0


class ProductLessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'status', 'viewing_time', 'last_viewed']

    def get_status(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.status if viewing else "Не просмотрено"

    def get_viewing_time(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.viewed_duration if viewing else 0

    def get_last_viewed(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.updated_at if viewing else None


# API для отображения статистики по продуктам
class ProductStatisticsSerializer(serializers.ModelSerializer):
    total_lessons_viewed = serializers.SerializerMethodField()
    total_time_spent = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'total_lessons_viewed', 'total_time_spent', 'total_students', 'purchase_percentage']

    def get_total_lessons_viewed(self, obj):
        return LessonViewing.objects.filter(lesson__products=obj).count()

    def get_total_time_spent(self, obj):
        return LessonViewing.objects.filter(lesson__products=obj).aggregate(Sum('viewed_duration'))['viewed_duration__sum'] or 0

    def get_total_students(self, obj):
        return obj.user_accesses.count()

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        users_with_access = obj.user_accesses.count()
        return (users_with_access / total_users) * 100 if total_users else 0

