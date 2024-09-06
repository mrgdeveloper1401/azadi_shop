from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Top_Students, Top_Teachers, Tajrobi_Top_Levels, Riazi_Top_Levels, Enasani_Top_Levels, Prizes, Obligations
from .serializers import TopTeachersSerializer, TopStudentsSerializer, TajrobiTopLevelsSerializer, RiaziTopLevelsSerializer, EnasaniTopLevelsSerializer, PrizesSerializer, ObligationsSerializer, CoursesSerializers
from courses.models import Course

class TopTeachersList(APIView):
    def get(self, request):
        top_teachers = Top_Teachers.objects.all()
        serializer = TopTeachersSerializer(top_teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopStudentsList(APIView):
    def get(self, request):
        top_students = Top_Students.objects.all()
        serializer = TopStudentsSerializer(top_students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TajrobiTopLevelsList(APIView):
    def get(self, request):
        tajrobi_top_levels = Tajrobi_Top_Levels.objects.all()
        serializer = TajrobiTopLevelsSerializer(tajrobi_top_levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RiaziTopLevelsList(APIView):
    def get(self, request):
        riazi_top_levels = Riazi_Top_Levels.objects.all()
        serializer = RiaziTopLevelsSerializer(riazi_top_levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EnasaniTopLevelsList(APIView):
    def get(self, request):
        enasani_top_levels = Enasani_Top_Levels.objects.all()
        serializer = EnasaniTopLevelsSerializer(enasani_top_levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PrizesList(APIView):
    def get(self, request):
        prizes = Prizes.objects.all()
        serializer = PrizesSerializer(prizes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ObligationsList(APIView):
    def get(self, request):
        obligations = Obligations.objects.all()
        serializer = ObligationsSerializer(obligations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowCourses(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CoursesSerializers(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)