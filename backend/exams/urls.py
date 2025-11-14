
from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add-exam/<int:exam_id>/', views.add_exam_view, name='add_exam'),
    path('about/', views.about_us_view, name='about_us'),
    path('contact/', views.contact_us_view, name='contact_us'),
    path('notice/<int:notice_id>/', views.notice_detail_view, name='notice_detail'),
]