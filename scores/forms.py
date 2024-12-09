from django import forms
from .models import Score
from django.core.exceptions import ValidationError
import datetime

class ScoreForm(forms.ModelForm):
    def __int__(self, *arg, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('grade').queryset = Grade.objects.all().order_by('grade_number')

    def clean_student_name(self):
        student_name = self.cleaned_data.get('student_name')
        if len(student_name) < 2 or len(student_name) > 50:
            raise ValidationError('Please enter correct student name')
        return student_name
        
    
    def clean_math_scores(self):
        math_score=self.cleaned_data.get('math_score')
        if not math_score or math_score < 0:
            raise ValidationError('Please enter a correct phone number')
        return math_score
    def clean_history_scores(self):

        history_score=self.cleaned_data.get('history_score')
        if not history_score or history_score < 0:
            raise ValidationError('Please enter a correct phone number')
        return history_score

    def clean_science_score(self):

        science_score=self.cleaned_data.get('science_score')
        if not science_score or science_score < 0:
            raise ValidationError('Please enter a correct phone number')
        return science_score

    class Meta:
        model = Score
        fields= ['title', 'grade', 'student_name', 'student_number', 'math_score', 'history_score', 'science_score']