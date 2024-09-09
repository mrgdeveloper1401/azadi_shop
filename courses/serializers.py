from rest_framework import serializers

from courses.models import Course, CourseCategory, DiscountCourse, Comment
from users.models import UserAccount


class CreatCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']

    def create(self, validated_data):
        course = Course.objects.get(slug=self.context['course_slug'])
        return Comment.objects.create(course=course, **validated_data)


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name")
    course = serializers.CharField(source="course.name")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'body', 'created_at', 'updated_at', 'public']


class CourseSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name", read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'user', 'category', 'name', 'slug', 'description', "price", 'final_price', 'sales',
                  'video', 'image', 'created_at', 'updated_at']

    def get_final_price(self, obj):
        return obj.final_price


class CategorySerializers(serializers.ModelSerializer):
    # children = serializers.SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class CourseDiscountSerializers(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = DiscountCourse
        fields = ['id', 'course', 'type', 'value', 'is_active', 'created_at', 'expired_date']

        extra_kwargs = {
            'expired_date': {
                'format': '%Y-%m-%dT%H:%M',  # فرمت خروجی
                'input_formats': ['%Y-%m-%dT%H:%M']  # فرمت ورودی
            }
        }
