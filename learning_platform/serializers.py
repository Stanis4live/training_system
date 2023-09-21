from rest_framework import serializers
from .models import Lesson, Product


class BaseLessonSerializer(serializers.ModelSerializer):
    def get_viewing(self, obj):
        user_viewings = self.context.get('request')._lesson_viewings_for_user
        return user_viewings.get(obj.id)


class LessonSerializer(BaseLessonSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'status', 'viewing_time']


    def get_status(self, obj):
        viewing = self.get_viewing(obj)
        return viewing.status if viewing else "Не просмотрено"

    def get_viewing_time(self, obj):
        viewing = self.get_viewing(obj)
        return viewing.viewed_duration if viewing else 0


class ProductLessonSerializer(BaseLessonSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'status', 'viewing_time', 'last_viewed']

    def get_status(self, obj):
        viewing = self.get_viewing(obj)
        return viewing.status if viewing else "Не просмотрено"

    def get_viewing_time(self, obj):
        viewing = self.get_viewing(obj)
        return viewing.viewed_duration if viewing else 0

    def get_last_viewed(self, obj):
        viewing = self.get_viewing(obj)
        return viewing.updated_at if viewing else None


class ProductStatisticsSerializer(serializers.ModelSerializer):
    total_lessons_viewed = serializers.SerializerMethodField()
    total_time_spent = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'total_lessons_viewed', 'total_time_spent', 'total_students', 'purchase_percentage']

    def get_total_lessons_viewed(self, obj):
        return obj.total_lessons_viewed

    def get_total_time_spent(self, obj):
        return obj.total_time_spent

    def get_total_students(self, obj):
        return obj.total_students

    def get_purchase_percentage(self, obj):
        return obj.purchase_percentage


