from django.db import models
from django.contrib.auth.models import User
from datetime import date

from grades.models import Grade
# Create your models here.
GENDER_CHOICES = [
    ('M', 'male'),
    ('F', 'female'),
]
class Student(models.Model):
    student_number = models.CharField(max_length = 20, unique=True, verbose_name = 'student number')
    student_name = models.CharField(max_length = 50, verbose_name = 'student name')
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, verbose_name = 'gender')
    birthday = models.DateField(verbose_name = 'date of birth', help_text = 'format: 2020-05-01', default=date.today)
    contact_number = models.CharField(max_length=20, verbose_name='contact number')
    address = models.TextField(verbose_name = 'address')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table="student"
        verbose_name_plural = "student info"
        verbose_name = "student info"
