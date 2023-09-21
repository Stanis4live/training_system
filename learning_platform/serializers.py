from rest_framework import serializers
from .models import Lesson, LessonViewing


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'duration', 'status', 'viewing_time']

    def get_status(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.status if viewing else "Не просмотрено"

    def get_viewing_time(self, obj):
        viewing = LessonViewing.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return viewing.viewed_duration if viewing else 0

