from django.urls import path

from images.views import show_image

app_name = 'images'
urlpatterns = [
    path('show_image/', show_image, name='show_image'),
]
