from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Score
from grades.models import Grade
from .forms import ScoreForm
from students.models import Student

# Create your views here.
class BaseScoreView():
    model = Score
    success_url = reverse_lazy('score_list')
    
class ScoreListView(BaseScoreView, ListView):
    template_name = 'scores/score_list.html'
    context_object_name = 'scores'
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
                Q(student_number=keyword) |
                Q(student_name=keyword)
            )
        return queryset

class ScoreCreateView(BaseScoreView, CreateView):
    template_name = 'scores/score_form.html'
    form_class = ScoreForm

    def form_valid(self, form):
        student_name = form.cleaned_data.get('student_name')
        student_number = form.cleaned_data.get('student_number')
        grade_id = form.cleaned_data.get('grade')

        # write into user table
        username = student_name + '_' + student_number 
        password = student_number[-6:]

        try:
            student = Student.objects.get(
                student_name=student_name,
                student_number=student_number,
                grade=grade_id
            )
        except Student.DoesNotExist:
            errors = {'general': [{'message': 'Student does not exist', 'code': 'not_found'}]}
            return JsonResponse({'status': 'error', 'messages': errors}, status=404)

        # write into student table
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

class ScoreUpdateView(BaseScoreView, UpdateView):
    template_name = 'scores/score_form.html'
    form_class = ScoreForm

    def form_valid(self, form):
        # get score object
        score = form.save(commit=False)
        # check if edited student_name/student number
        if 'student_name' or 'student_number' in form.changed_date:
            try:
                student = Student.objects.get(
                    student_name=score.student_name,
                    student_number=score.student_number,
                    grade=score.grade_id
                )
            except Student.DoesNotExist:
                errors = {'general': [{'message': 'Student does not exist', 'code': 'not_found'}]}
                return JsonResponse({'status': 'error', 'messages': errors}, status=404)


        score.save()
        
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

class ScoreDeleteView(BaseScoreView, DeleteView):

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

class ScoreDeleteMultipleView(ScoreDeleteView):
    pass

def upload_scores():
    pass 
def export_scores():
    pass 
class MyScoreListView(ListView):
    pass
