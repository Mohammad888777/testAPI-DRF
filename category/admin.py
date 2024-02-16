from django.contrib import admin

# Register your models here.
from .models import Teacher,TeacherFeather,Category



admin.site.register(
    [
        Teacher,TeacherFeather,Category
    ]
)