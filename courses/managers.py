from django.db.models import Manager
from treebeard.mp_tree import MP_NodeManager

from core.datetime_config import now


class CategoryManager(MP_NodeManager):
    def is_publish(self):
        return self.filter(is_public=True)


class CourseManager(Manager):
    def is_active(self):
        return self.filter(is_active=True)


class DiscountManager(Manager):
    def delete_discount(self):
        return self.filter(expired_date__lt=now).delete()
