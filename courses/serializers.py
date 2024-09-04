from rest_framework import serializers
from .models import Course, CourseCategory, DiscountCourse, Comment


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'icon', 'created_at', 'updated_at']


class CourseDiscountSerializers(serializers.ModelSerializer):
    class Meta:
        model = DiscountCourse
        fields = '__all__'

        extra_kwargs = {
            'expired_date': {
                'format': '%Y-%m-%dT%H:%M',  # فرمت خروجی
                'input_formats': ['%Y-%m-%dT%H:%M']  # فرمت ورودی
            }
        }


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'body', 'admin_response', 'created', 'updated', 'public']
        read_only_fields = ['created', 'updated', 'admin_response']


class CourseSerializers(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CourseCategory.objects.all())
    id = serializers.IntegerField(read_only=True)
    total_price = serializers.SerializerMethodField()
    course_discount = CourseDiscountSerializers(many=True, read_only=True)
    ccomment = CommentSerializers(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'user', 'category', 'name', 'slug', 'desc',
                  'price', 'total_price', 'course_discount', 'sales',
                  'video', 'image', 'created_at', 'updated_at', 'ccomment']

    def get_total_price(self, obj):
        return obj.get_total_price