from django.contrib import admin
from .models import Product, Lesson, ProductAccess, LessonViewing

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(ProductAccess)
admin.site.register(LessonViewing)
