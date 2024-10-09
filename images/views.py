from django.shortcuts import render
from images.models import Image


def show_image(request):
    latest_image = Image.objects.get(id=19)
    return render(request, 'show_images.html', {'image': latest_image})
