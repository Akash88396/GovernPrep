# tests/models.py

from django.db import models
from decimal import Decimal 
from exams.models import Exam  # exams app se Exam model ko import karein
from django.contrib.auth.models import User # Django ke default User model ko import karein

# ==============================================================================
# QUESTION BANK MODELS
# Yeh models aapke "Question Bank" ko banate hain.
# ==============================================================================

class Question(models.Model):
    """
    Har question ab seedhe ek 'Exam' se judega, 'MockTest' se nahi.
    Yeh humara "Question Bank" hai.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Choice(models.Model):
    """
    Har question ke liye multiple choices (options).
    Yeh model Question se juda hai.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        # Admin panel mein behtar display ke liye
        return f"{self.question.text[:50]}... -> {self.text}"

# ==============================================================================
# MOCK TEST MODELS
# Yeh models asli mock test aur uske results ko define karte hain.
# ==============================================================================

class MockTest(models.Model):
    """
    Yeh model ab sirf test ke 'niyam' (rules) store karta hai, questions nahi.
    Jaise, test ka naam kya hai, usmein kitne questions aayenge, etc.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='mocktests')
    title = models.CharField(max_length=200)
    number_of_questions = models.IntegerField(default=100)
    duration_minutes = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=100)

    negative_marks_per_question = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.25'))
    
    questions = models.ManyToManyField(Question, blank=True, related_name='mock_tests')
    
   
   
    def __str__(self):
        return f"{self.exam.title} - {self.title}"

class TestResult(models.Model):
    """
    User dwara diye gaye har mock test ke result ko store karta hai.
    (Ise naye fields ke saath update kar diya gaya hai)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    
    # === YAHAN BADLAV KIYA GAYA HAI ===
    
    # Score mein decimal (jaise 10.25) ho sakta hai, isliye IntegerField se behtar hai
    score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Aapke purane 'total' field ko 'total_marks' se badal diya gaya hai
    total_marks = models.IntegerField()
    
    # Yeh 3 naye fields (khaane) add kiye gaye hain
    total_correct = models.IntegerField(default=0)
    total_incorrect = models.IntegerField(default=0)
    total_unanswered = models.IntegerField(default=0)
    
    # === BADLAV YAHAN KHATAM HOTA HAI ===
    
    timestamp = models.DateTimeField(auto_now_add=True)
    question_ids = models.JSONField(default=list) # Yeh field waisa hi hai

    def __str__(self):
        return f"{self.user.username} - {self.mock_test.title}"