from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html

from tests.models import Question, Choice, MockTest
from .forms import CsvUploadForm
from .models import Exam, ExamCategory, ContactMessage ,Notice
import csv
import io

@admin.register(ExamCategory)
class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'upload_questions_link')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/upload-questions/', self.admin_site.admin_view(self.upload_questions_view), name='exams_exam_upload_questions'),
        ]
        return custom_urls + urls

    def upload_questions_link(self, obj):
        return format_html('<a class="button" href="{}">Manage Question Bank</a>', f'{obj.id}/upload-questions/')
    upload_questions_link.short_description = 'Bulk Upload'
    
    def upload_questions_view(self, request, object_id):
        exam = self.get_object(request, object_id)
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():
                upload_type = form.cleaned_data['upload_type']
                csv_file = request.FILES['csv_file']
                
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'This is not a CSV file')
                    return redirect('.')
                
                try:
                    if upload_type == 'replace':
                        old_mock_tests_count = exam.mocktests.count()
                        exam.mocktests.all().delete()
                        exam.questions.all().delete()
                        messages.warning(request, f"REPLACED: All old questions and {old_mock_tests_count} mock tests were deleted.")
                    
                    # === YAHAN BADLAV KIYA GAYA HAI ===
                    # "utf-8" ko "utf-8-sig" se badla gaya hai
                    file_data = csv_file.read().decode("utf-8-sig")
                    reader = csv.DictReader(io.StringIO(file_data))
                    
                    questions_created_count = 0
                    for row in reader:
                        question_text = row.get('question_text', '').strip()
                        choices_text = [
                            row.get('choice1', '').strip(),
                            row.get('choice2', '').strip(),
                            row.get('choice3', '').strip(),
                            row.get('choice4', '').strip()
                        ]
                        correct_choice_number_str = row.get('correct_choice', '0').strip()

                        if not question_text or not all(choices_text) or not correct_choice_number_str.isdigit():
                            continue
                        
                        correct_choice_number = int(correct_choice_number_str)

                        if correct_choice_number not in [1, 2, 3, 4]:
                            continue

                        correct_choice_text = choices_text[correct_choice_number - 1]
                        
                        question = Question.objects.create(exam=exam, text=question_text)
                        for choice_text in choices_text:
                            is_correct = (choice_text == correct_choice_text)
                            Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                        questions_created_count += 1
                    
                    if upload_type == 'append':
                        messages.success(request, f'{questions_created_count} new questions have been ADDED to the "{exam.title}" question bank.')
                    else:
                        messages.success(request, f'{questions_created_count} new questions have been UPLOADED to the fresh "{exam.title}" question bank.')
                    
                    return redirect('..')
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")

        form = CsvUploadForm()
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = f'Manage Question Bank for {exam.title}'
        context['exam'] = exam
        return render(request, 'admin/exams/exam/upload_questions.html', context)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin panel mein "Contact messages" section ko manage karne ke liye.
    """
    # List mein yeh columns dikhayein
    list_display = ('name', 'email', 'timestamp', 'is_read')
    
    # In cheezon ke hisab se filter karne ka option dein
    list_filter = ('is_read', 'timestamp')
    
    # Admin messages ko edit na kar sake, sirf dekh sake
    readonly_fields = ('name', 'email', 'message', 'timestamp')

    def has_add_permission(self, request):
        # Admin ko naye message add karne ka option na dein
        return False
    
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')   