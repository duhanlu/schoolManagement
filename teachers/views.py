from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import Teacher
from teachers.forms import TeacherForm
from grades.models import Grade
# Create your views here.

class BasaeTeacherView(): 
    model = Teacher
    success_url = reverse_lazy('teachers_list')


class TeacherListView(BasaeTeacherView, ListView):
    template_name = 'teachers/teachers_list.html'
    context_object_name = 'teachers'
    paginate_by = 10

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
                Q(phone_number=keyword) |
                Q(teacher_name=keyword)
            )
        return queryset

class TeacherCreateView(BasaeTeacherView, CreateView):
    model = Teacher
    template_name = 'teachers/teacher_form.html'
    form_class = TeacherForm

    def form_valid(self, form):
        teacher_name = form.cleaned_data.get('teacher_name')
        phone_number = form.cleaned_data.get('phone_number')

        # write into user table
        username = teacher_name + '_' + phone_number 
        password = phone_number[-6:]
        users = User.objects.filter(username=username)

        if users.exists():
            user = users.first()
        else:
            user = User.objects.create_user(username=username, password=password)
        # write into teacher table
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


class TeacherUpdateView(BasaeTeacherView, UpdateView):
    model = Teacher
    template_name = 'teachers/teacher_form.html'
    form_class = TeacherForm

    def form_valid(self, form):
        # get student object
        teacher = form.save(commit=False)
        # check if edited student_name/student number
        if 'teacher_name' or 'phone_number' in form.changed_date:
            teacher.user.username = form.cleaned_data.get('teacher_name') + form.cleaned_data.get('phone_number')
            teacher.user.password = make_password(form.cleaned_data.get('phone_number')[-6:])
            teacher.user.save()

        teacher.save()
        
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

class TeacherDeleteView(BasaeTeacherView, DeleteView):
    success_url = reverse_lazy('teacher_list')
    model = Teacher

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