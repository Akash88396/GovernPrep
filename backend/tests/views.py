# tests/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MockTest, Question, Choice, TestResult

@login_required
def test_view(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, pk=mock_test_id)
    questions = mock_test.questions.all()
    
    marks_per_question = 0
    if mock_test.number_of_questions > 0:
        marks_per_question = mock_test.total_marks / mock_test.number_of_questions
        
    context = {
        'mock_test': mock_test,
        'questions': questions,
        'marks_per_question': marks_per_question,
    }
    return render(request, 'tests/test.html', context)

@login_required
def result_view(request, mock_test_id):
    if request.method != 'POST':
        return redirect('tests:test_view', mock_test_id=mock_test_id)

    mock_test = get_object_or_404(MockTest, pk=mock_test_id)
    questions = mock_test.questions.all()
    
    marks_per_question = 0
    if mock_test.number_of_questions > 0:
        marks_per_question = mock_test.total_marks / mock_test.number_of_questions

    score = 0
    correct_answers = 0
    incorrect_answers = 0
    
    # === YAHAN SE NAYA LOGIC SHURU HOTA HAI ===
    detailed_results = []

    for question in questions:
        selected_choice_id = request.POST.get(f'question_{question.id}')
        correct_choice = question.choices.get(is_correct=True)
        
        status = ''
        selected_choice = None

        if selected_choice_id:
            try:
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                if selected_choice.question == question and selected_choice.is_correct:
                    score += marks_per_question
                    correct_answers += 1
                    status = 'correct'
                else:
                    score -= float(mock_test.negative_marks_per_question)
                    incorrect_answers += 1
                    status = 'incorrect'
            except (ValueError, Choice.DoesNotExist):
                status = 'skipped' # Agar galat value aayi to use skipped maanein
        else:
            status = 'skipped'
        
        detailed_results.append({
            'question': question,
            'selected_choice': selected_choice,
            'correct_choice': correct_choice,
            'status': status
        })

    skipped_answers = questions.count() - (correct_answers + incorrect_answers)
    percentage = round((score / mock_test.total_marks) * 100) if mock_test.total_marks > 0 else 0

    TestResult.objects.create(user=request.user, mock_test=mock_test, score=score, total=mock_test.total_marks)

    context = {
        'mock_test': mock_test,
        'marks_obtained': score,
        'total_marks_of_test': mock_test.total_marks,
        'percentage': percentage,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'skipped_answers': skipped_answers,
        'detailed_results': detailed_results, # Poori analysis list ko template mein bhejein
    }
    return render(request, 'tests/result.html', context)