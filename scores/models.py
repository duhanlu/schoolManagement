from django.db import models

from students.models import Grade
# Create your models here.

class Score(models.Model):
    title = models.CharField(max_length=20, help_text='exam name', verbose_name='exam name')
    student_number = models.CharField(max_length=20, verbose_name='student number')
    student_name = models.CharField(max_length=20, help_text='name', verbose_name='student name')
    math_score = models.DecimalField(max_digits=5, decimal_places=2, help_text='math scores')
    history_score = models.DecimalField(max_digits=5, decimal_places=2, help_text='history scores')
    science_score = models.DecimalField(max_digits=5, decimal_places=2, help_text='science_score')

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='score', verbose_name='class')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = 'score'
        verbose_name_plural = "score info"
        verbose_name = 'score info'