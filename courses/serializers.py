from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema_field

from courses.models import Course, CourseCategory, DiscountCourse, Comment
from professors.models import Professor
from users.models import UserAccount


class CreatCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', "rating"]

    def create(self, validated_data):
        course = Course.objects.get(slug=self.context['course_slug'])
        return Comment.objects.create(course=course, **validated_data)


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.mobile_phone")
    course = serializers.CharField(source="course.name")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', "rating", 'body', 'created_at', 'updated_at', 'public']


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['rating', "body"]


class SimpleProfessorSerializer(serializers.ModelSerializer):
    professor_image = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ["first_name", "last_name", "professor_image"]

    def get_professor_image(self, obj):
        return obj.professor_image.image_url


class SimpleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ['name']


class CourseSerializers(serializers.ModelSerializer):
    professor = SimpleProfessorSerializer()
    course_image = serializers.SerializerMethodField()
    category = SimpleCategorySerializer()
    # final_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = ['image']

    def get_course_image(self, obj):
        if obj.image:
            return obj.image.image_url
        return None

    # def get_final_price(self, obj):
        # discount = obj.course_discount.filter(is_active=True, expired_date__gt=now())
        # discount = obj.course_discount.all()
        # f = obj.price
        # for d in discount:
        #     f = d.calc_price(f)
        # return f


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class CategoryTreeSerializers(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields = '__all__'

    def get_children(self, obj):
        return CategorySerializers(obj.get_children(), many=True).data


class CategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


CategoryTreeSerializers.get_children = extend_schema_field(serializers.ListField(child=CategorySerializers())) \
    (CategoryTreeSerializers.get_children)
