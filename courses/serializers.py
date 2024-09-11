from rest_framework import serializers

from courses.models import Course, CourseCategory, DiscountCourse, Comment
from users.models import UserAccount


class CreatCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', "rating"]

    def create(self, validated_data):
        course = Course.objects.get(slug=self.context['course_slug'])
        return Comment.objects.create(course=course, **validated_data)


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name")
    course = serializers.CharField(source="course.name")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', "rating", 'body', 'created_at', 'updated_at', 'public']


class CourseSerializers(serializers.ModelSerializer):
    professor = serializers.CharField(source="professor.get_full_name")

    class Meta:
        model = Course
        fields = ['id', 'professor', 'category', 'name', 'slug', 'description', "price", 'final_price', 'sales',
                  'video', 'show_image_url', 'created_at', 'updated_at']


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ['id', 'name', "numchild", "path", "depth"]

