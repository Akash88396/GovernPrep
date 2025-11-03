# tests/admin.py

from django.contrib import admin, messages
from .models import MockTest, TestResult, Question
import random

# YEH NAYA SECTION ADD KIYA GAYA HAI
# Yeh questions ki ek read-only list dikhayega
class QuestionInlineReadOnly(admin.TabularInline):
    model = MockTest.questions.through # ManyToMany relationship ke through table ko target karein
    extra = 0 # Naye question add karne ka option na dein
    can_delete = False # Delete karne ka option na dein
    readonly_fields = ['question'] # Question field ko read-only banayein
    verbose_name = "Assigned Question"
    verbose_name_plural = "Assigned Questions"

    def has_add_permission(self, request, obj=None):
        return False # Add button ko poori tarah se hata dein

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):

    
    list_display = ('title', 'exam', 'number_of_questions', 'get_question_count')
    list_filter = ('exam',)
    
    # Is page se jude hue questions ko dikhane ke liye inline add karein
    inlines = [QuestionInlineReadOnly]

    # Fields ko sections mein baantein
    fieldsets = (
        ('Mock Test Details', {
            'fields': ('exam', 'title')
        }),
        ('Test Rules & Marking', {
            # 'negative_marks_per_question' ko form mein add karein
            'fields': ('number_of_questions', 'duration_minutes', 'total_marks', 'negative_marks_per_question')
        }),
    )
    
    def get_question_count(self, obj):
        return obj.questions.count()
    get_question_count.short_description = 'Assigned Questions'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and obj.questions.count() == 0:
            question_bank = list(obj.exam.questions.all())
            if not question_bank:
                messages.warning(request, f"Could not assign questions. The question bank for '{obj.exam.title}' is empty.")
                return
            num_to_select = min(obj.number_of_questions, len(question_bank))
            if num_to_select > 0:
                selected_questions = random.sample(question_bank, num_to_select)
                obj.questions.set(selected_questions)
                messages.success(request, f"{len(selected_questions)} questions were randomly assigned.")
            else:
                messages.warning(request, "Number of questions to select was zero.")

admin.site.register(TestResult)