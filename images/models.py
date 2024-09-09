from django.db import models
from hashlib import sha1
from rest_framework.exceptions import ValidationError

from core.models import CreateMixin, UpdateMixin


class Image(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(width_field="width", height_field="height", upload_to="images/%Y/%m/%d")

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    file_hash = models.CharField(max_length=40, db_index=True, null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)

    focal_point_x = models.PositiveIntegerField(null=True, blank=True)
    focal_point_y = models.PositiveIntegerField(null=True, blank=True)
    focal_point_width = models.PositiveIntegerField(null=True, blank=True)
    focal_point_height = models.PositiveIntegerField(null=True, blank=True)

    @property
    def generate_hash(self):
        hasher = sha1()
        for c in self.image.chunks():
            hasher.update(c)
        return hasher.hexdigest()

    def __str__(self):
        return f"{self.file_hash} && {self.title}"

    def save(self, *args, **kwargs):
        self.file_hash = self.generate_hash
        self.file_size = self.image.size
        if Image.objects.filter(file_hash=self.file_hash).exists():
            raise ValidationError("Image already exists")
        super().save(*args, **kwargs)
