# tests/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MockTest, Question, Choice, TestResult
from decimal import Decimal # Negative marking ke liye Decimal ka istemal karein (float se behtar)

@login_required
def test_view(request, mock_test_id):
    # Yeh function bilkul sahi hai, ismein koi badlav nahi
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
    
    # === YAHAN BADLAV KIYA GAYA HAI (Crash Fix) ===
    # Sab kuch Decimal mein karein taaki float aur decimal ka error na aaye
    
    marks_per_question = Decimal(0)
    if mock_test.number_of_questions > 0:
        # float (/) ki jagah Decimal division (/) ka istemal karein
        marks_per_question = Decimal(mock_test.total_marks) / Decimal(mock_test.number_of_questions)

    score = Decimal(0) # score ko bhi Decimal banayein
    # === BADLAV YAHAN KHATAM HOTA HAI ===
    
    correct_answers = 0
    incorrect_answers = 0
    
    # Negative marks ko surakshit tareeke se handle karein (Aapka yeh code sahi tha)
    try:
        negative_marks = mock_test.negative_marks_per_question
        if negative_marks is None:
            negative_marks = Decimal(0.0)
    except (ValueError, TypeError):
        negative_marks = Decimal(0.0)
    
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
                    score += marks_per_question # Ab yeh Decimal + Decimal hai (OK)
                    correct_answers += 1
                    status = 'correct'
                else:
                    score -= negative_marks # Ab yeh Decimal - Decimal hai (OK)
                    incorrect_answers += 1
                    status = 'incorrect'
            except (ValueError, Choice.DoesNotExist):
                status = 'skipped'
        else:
            status = 'skipped'
        
        detailed_results.append({
            'question': question,
            'selected_choice': selected_choice,
            'correct_choice': correct_choice,
            'status': status
        })

    skipped_answers = questions.count() - (correct_answers + incorrect_answers)
    
    # === YAHAN BADLAV KIYA GAYA HAI (Crash Fix) ===
    # Score ko 0 se neeche nahi jaane dena
    if score < Decimal(0): # Ise bhi Decimal(0) se compare karein
        score = Decimal(0)
    
    percentage = Decimal(0)
    if mock_test.total_marks > 0:
         # Is calculation ko bhi safe (Decimal) banayein
         percentage = round((score / Decimal(mock_test.total_marks)) * Decimal(100), 2)
    # === BADLAV YAHAN KHATAM HOTA HAI ===
        
    TestResult.objects.create(
        user=request.user, 
        mock_test=mock_test, 
        score=round(score, 2), # Aapka yeh code sahi tha
        total_marks=mock_test.total_marks,
        total_correct=correct_answers,
        total_incorrect=incorrect_answers,
        total_unanswered=skipped_answers
    )

    context = {
        'mock_test': mock_test,
        'marks_obtained': score,
        'total_marks_of_test': mock_test.total_marks,
        'percentage': percentage,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'skipped_answers': skipped_answers,
        'detailed_results': detailed_results,
    }
    return render(request, 'tests/result.html', context)