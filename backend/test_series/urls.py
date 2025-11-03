from django.urls import path
from . import views

app_name = 'test_series'

urlpatterns = [
    path('', views.my_test_series_view, name='my_tests'),
    path('exam/<int:exam_id>/', views.mock_test_list_view, name='mock_test_list'),
]
