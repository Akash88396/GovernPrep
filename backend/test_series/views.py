from django.shortcuts import render, get_object_or_404
from exams.models import Exam 
# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required
def my_test_series_view(request):
    # Current user ke saare subscribed exams ko fetch karein
    subscribed_exams = request.user.subscribed_exams.all()
    context = {
        'subscribed_exams': subscribed_exams
    }
    return render(request, 'test_series/my_tests.html', context)

@login_required
def mock_test_list_view(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    mock_tests = exam.mocktests.all()
    context = {
        'exam': exam,
        'mock_tests': mock_tests
    }
    return render(request, 'test_series/mock_test_list.html', context)