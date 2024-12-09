from django import forms
from .models import Student 
from django.core.exceptions import ValidationError
import datetime

class StudentForm(forms.ModelForm):
    def __int__(self, *arg, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('grade').queryset = Grade.objects.all().order_by('grade_number')

    def clean_student_name(self):
        student_name = self.cleaned_data.get('student_name')
        if len(student_name) < 2 or len(student_name) > 50:
            raise ValidationError('Please enter correct student name')
        return student_name
        
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if not isinstance(birthday, datetime.date):
            raise ValidationError('Birth Date Format is incorrect, correct format is 2024-05-01')
        if birthday > datetime.date.today():
            raise ValidationError('Error Birth date')
        return birthday
    
    def clean_contact_number(self):
        contact_number=self.cleaned_data.get('contact_number')
        if len(contact_number) != 10:
            raise ValidationError('Please enter a correct phone number')
        return contact_number

    class Meta:
        model = Student
        fields= ['student_name', 'student_number', 'grade', 'gender', 'birthday', 'contact_number', 'address']