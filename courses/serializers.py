from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, DecimalField

from courses.models import Course, CourseCategory, Comment, DiscountCourse
from professors.models import Professor


class CreatCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', "rating"]

    def create(self, validated_data):
        course = Course.objects.get(slug=self.context['course_slug'])
        return Comment.objects.create(course=course, **validated_data)


class CommentSerializers(ModelSerializer):
    user = CharField(source="user.mobile_phone")
    course = CharField(source="course.name")

    class Meta:
        model = Comment
        fields = "__all__"


class UpdateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['rating', "body"]


class SimpleProfessorSerializer(ModelSerializer):
    professor_image = SerializerMethodField()

    class Meta:
        model = Professor
        fields = ["first_name", "last_name", "professor_image"]

    def get_professor_image(self, obj):
        return obj.professor_image.url if obj.professor_image else None


class SimpleCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['name']


class CourseSerializers(ModelSerializer):
    professor = SimpleProfessorSerializer()
    category = SimpleCategorySerializer(many=True)
    final_price = DecimalField(max_digits=12, decimal_places=2, read_only=True)
    discount_value = DecimalField(max_digits=12, decimal_places=2, read_only=True)
    image_url = SerializerMethodField()

    class Meta:
        model = Course
        exclude = ['image']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class CategorySerializers(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug', "depth", "path", "numchild", "icon", "children"]


class SimpleCourseSerializer(ModelSerializer):
    professor = CharField()

    class Meta:
        model = Course
        fields = ['id', "name", "show_image_url", "professor", "price", "calc_final_price"]


class DiscountCourseSerializer(ModelSerializer):
    course = SimpleCourseSerializer()

    class Meta:
        model = DiscountCourse
        fields = '__all__'
