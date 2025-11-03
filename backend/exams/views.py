# exams/views.py

from django.shortcuts import render, redirect, get_object_or_404 # redirect aur get_object_or_404 add karein
from django.contrib.auth.decorators import login_required # Ise import karein
from .models import Exam, ExamCategory
from django.contrib.auth.models import User 
from tests.models import MockTest
from .forms import ContactForm 
from django.contrib import messages 
from .models import ContactMessage



def home_view(request):
    categories = ExamCategory.objects.prefetch_related('exams').all()
    
    # === YAHAN BADLAV KIYA GAYA HAI ===
    
    # Sahi count calculate karein
    category_count = ExamCategory.objects.count()
    mock_test_count = MockTest.objects.count() # Total mock tests ka count
    aspirant_count = User.objects.count()
    
    context = {
        'categories': categories,
        'category_count': category_count,
        'mock_test_count': mock_test_count, # Naya variable context mein bhejein
        'aspirant_count': aspirant_count,
    }
    return render(request, 'exams/home.html', context)


def about_us_view(request):
    return render(request, 'exams/about_us.html')

def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form se data nikalein
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile= form.cleaned_data['mobile_number']
            message_text = form.cleaned_data['message']

            # Naya ContactMessage object banakar database mein save karein
            ContactMessage.objects.create(
                name=name,
                email=email,
                mobile_number=mobile,
                message=message_text
            )
            
            messages.success(request, f'Thank you for your message, {name}! We will get back to you shortly.')
            return redirect('exams:contact_us')
    else:
        form = ContactForm()
        
    return render(request, 'exams/contact_us.html', {'form': form})


@login_required
def add_exam_view(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    exam.subscribers.add(request.user)
    # User ko wapas homepage par bhej dein
    return redirect('exams:home')