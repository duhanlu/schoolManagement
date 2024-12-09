from django.db import models

# Create your models here.
class Grade(models.Model):
    grade_name = models.CharField(max_length = 50, unique = True, verbose_name = 'class name')
    grade_number = models.CharField(max_length = 10, unique = True, verbose_name='class number')

    def __str__(self) -> str:
        return self.grade_name
    
    class Meta:
        db_table = 'grade'
        verbose_name = 'class'
        verbose_name_plural = 'class name'
    