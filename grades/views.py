from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.db.models import Q
from django.urls import reverse_lazy

from .form import GradeForm
from .models import Grade
from utils.permissions import RoleRequiredMixin
# Create your views here.
class GradeListView(RoleRequiredMixin, ListView):
    model = Grade
    context_object_name = 'grades'

class GradeListView(GradeListView, ListView):
    template_name = 'grades/grades_list.html'
    fields = ['grade_name', 'grade_number']
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(grade_name__icontains=search) |
                Q(grade_number__icontains=search)
            )
        return queryset
class GradeCreateView(GradeListView, CreateView):
    template_name = 'grades/grade_form.html'
    form_class = GradeForm
    success_url = reverse_lazy('grades_list')

class GradeUpdateView(GradeListView, UpdateView): 
    template_name = 'grades/grade_form.html'
    form_class = GradeForm
    success_url = reverse_lazy('grades_list')

class GradeDeleteView(GradeListView, DeleteView):
    template_name = 'grades/grade_delete_confirm.html'
    success_url = reverse_lazy('grades_list')