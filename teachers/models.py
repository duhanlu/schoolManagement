from django.db import models
from django.contrib.auth.models import User

from grades.models import Grade

# Create your models here.
GENDER_CHOICES = [
    ('M', 'MALE'),
    ('F', 'FEMALE'),
]

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    teacher_name = models.CharField(max_length=50, verbose_name='teacher name')
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='phone number')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='gender')
    birthday = models.DateField(verbose_name='birthday', help_text='format: 2020-05-01')
    grade = models.OneToOneField(Grade, on_delete=models.DO_NOTHING, verbose_name='manage class')

    def __str__(self) -> str:
        return self.teacher_name
    
    class Meta:
        db_table = 'teacher'
        verbose_name_plural = 'teacher info'
        verbose_name = 'teacher info'