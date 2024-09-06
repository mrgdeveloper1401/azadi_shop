from django.urls import path
from .views import TopTeachersList, TopStudentsList, TajrobiTopLevelsList, RiaziTopLevelsList, EnasaniTopLevelsList, PrizesList, ObligationsList, ShowCourses

urlpatterns = [
    path('api/top-teachers/', TopTeachersList.as_view(), name='top-teachers-list'),
    path('api/top-students/', TopStudentsList.as_view(), name='top-students-list'),
    path('api/tajrobi-top-levels/', TajrobiTopLevelsList.as_view(), name='tajrobi-top-levels-list'),
    path('api/riazi-top-levels/', RiaziTopLevelsList.as_view(), name='riazi-top-levels-list'),
    path('api/enasani-top-levels/', EnasaniTopLevelsList.as_view(), name='enasani-top-levels-list'),
    path('api/prizes/', PrizesList.as_view(), name='prizes-list'),
    path('api/obligations/', ObligationsList.as_view(), name='obligations-list'),
    path('api/courses/', ShowCourses.as_view(), name='courses-list'),
]