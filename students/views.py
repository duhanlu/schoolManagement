from pathlib import Path
import json
from io import BytesIO

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import Student
from .forms import StudentForm
from django.urls import reverse_lazy
from utils.handle_excel import ReadExcel
from grades.models import Grade
from utils.permissions import RoleRequiredMixin

import openpyxl
# Create your views here.

class BasestudentView(RoleRequiredMixin): 
    model = Student
    context_object_name = 'students'
    allowed_roles = ['admin', 'teacher']

class StudentListView(BasestudentView, ListView):
    template_name = 'students/students_list.html'
    paginate_by = 10
    ordering = ['student_number']

    def get_context_data(self):
        context = super().get_context_data()
        context["grades"] = Grade.objects.all() .order_by('grade_number')
        context['current_grade'] = self.request.GET.get('grade', '')
        return context
    

    def get_queryset(self):
        queryset = super().get_queryset()
        grade_id = self.request.GET.get('grade')
        keyword = self.request.GET.get('search')
        if grade_id:
            queryset = queryset.filter(grade__pk=grade_id)
        if keyword:
            queryset = queryset.filter(
                Q(student_number=keyword) |
                Q(student_name=keyword)
            )
        return queryset

class StudentCreateView(BasestudentView, CreateView):
    template_name = 'students/student_form.html'
    form_class = StudentForm

    def form_valid(self, form):
        student_name = form.cleaned_data.get('student_name')
        student_number = form.cleaned_data.get('student_number')

        # write into user table
        username = student_name + '_' + student_number 
        password = student_number[-6:]
        users = User.objects.filter(username=username)

        if users.exists():
            user = users.first()
        else:
            user = User.objects.create_user(username=username, password=password)
        # write into student table
        form.instance.user = user
        form.save()

        return JsonResponse({
            'status': 'success',
            'messages': 'successful operation',
        },status = 200
        )
    
    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({
            'status': 'error',
            'messages': errors,
        }, status= 400)

class StudentUpdateView(BasestudentView, UpdateView):
    template_name = 'students/student_form.html'
    form_class = StudentForm

    def form_valid(self, form):
        # get student object
        student = form.save(commit=False)
        # check if edited student_name/student number
        if 'student_name' or 'student_number' in form.changed_date:
            student.user.username = form.cleaned_data.get('student_name') + form.cleaned_data.get('student_number')
            student.user.password = make_password(form.cleaned_data.get('student_number')[-6:])
            student.user.save()

        student.save()
        
        return JsonResponse({
            'status': 'success',
            'messages': 'successful operation',
        },status = 200
        )

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({
            'status': 'error',
            'messages': errors,
        }, status= 400)

class StudentDeleteView(BasestudentView, DeleteView):
    success_url = reverse_lazy('student_list')
    model = Student

    def delete(self, requst, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({
                'status': 'success',
                'messages': 'Delete Successfully'
            }, status = 200)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'messages': 'Delete Unsuccessfully' + str(e)
            }, status = 500)

class StudentBulkDeleteView(BasestudentView, DeleteView): 
    model = Student
    success_url = reverse_lazy('student_list')
    def post(self, request, *arg, **kwargs):
        selected_ids = request.POST.getlist('student_ids')
        if not selected_ids:
            return JsonResponse({
                'status': 'error',
                'messages': 'Please choose students you want to delete'
            }, status = 400)
        self.object_list = self.get_queryset().filter(id__in = selected_ids)
        try: 
            self.object_list.delete()
            return JsonResponse({
                'status': 'success',
                'messages': 'Delete Successfully'
            })
        except Exception as e: 
            return

def upload_student(request):
    
    if request.method == 'POST':
        file = request.FILES.get('excel_file')
        # check if uploaded a file
        if not file:
            return JsonResponse({
                'status': 'error',
                'messages': 'Please upload excel file'
            }, status = 400)

        # check file format
        ext = Path(file.name).suffix
        if ext.lower() != '.xlsx':
            return JsonResponse({
                'status': 'error',
                'messages': 'Please upload a valid file'
            }, status = 400)
        # read data
        read_excel = ReadExcel(file)
        data = read_excel.get_data()
        if data[0] != ['class', 'student name', 'student number', 'gender', 'birthday', 'contact number', 'address']:
            return JsonResponse({
                'status': 'error',
                'messages': 'Format in excel is incorrect'
            })
        
        for row in data[1:]:
            grade, student_name, student_number, gender, birthday, contact_number, address = row
            # check information
            grade = Grade.objects.filter(grade_name = grade).first()
            if not grade:
                return JsonResponse({
                    'status': 'error',
                    'messages': f'{grade} does not exist'
                }, status = 400)
            # write data into database
            try: 
                student_number = str(student_number)
                username = student_name + '_' + student_number
                users = User.objects.filter(username=username)
                if users.exists():
                    user = users.first()
                else:
                    
                    password = student_number[-6:]
                    user = User.objects.create_user(username=username, password=password)

                Student.objects.create(
                    student_number = student_number,
                    student_name = student_name,
                    gender = gender,
                    birthday = birthday,
                    contact_number = contact_number,
                    address = address,
                    user = user,
                    grade = grade
                )
            except Exception as e: 
                print(f"Error occurred: {e}")
                return JsonResponse({'status': 'error', 'messages': 'Fail to upload'}, status = 500)
        return JsonResponse({
                    'status': 'success',
                    'messages': "Upload successfully!"
        }, status = 200)

def export_excel(request):
    if request.method == 'POST': 
        data = json.loads(request.body)
        grade_id = data.get('grade')
        # check if grade id exist
        if not grade_id:
            return JsonResponse({'status': 'error', 'messages': 'No class value'}, status = 404)
        try: 
            grade = Grade.objects.get(id = grade_id)
        except Grade.DoesNotExist:
            return JsonResponse({'status': 'error', 'messages': 'Class does not exist'}, status = 404)
        
        students = Student.objects.filter(grade = grade)
        if not students.exists():
            return JsonResponse({'status': 'error', 'messages': 'No Student Information found'}, status = 404)
        
        wb = openpyxl.Workbook()
        ws = wb.active

        column = ['class', 'student name', 'student number', 'gender', 'birthday', 'contact number', 'address']
        ws.append(column)
        for student in students:
            ws.append([student.grade.grade_name, student.student_name, student.student_number, student.gender, student.birthday, student.contact_number, student.address])
        
        # save excel 
        excel_file = BytesIO()
        wb.save(excel_file)
        wb.close()

        # reset file pointer
        excel_file.seek(0)

        # set response
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="students.xlsx" '
        return response
