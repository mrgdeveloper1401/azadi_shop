from django.urls import path
from .views import HomePageApiView


app_name = 'home'
urlpatterns = [
    path('', HomePageApiView.as_view(), name='homepage'),
]
