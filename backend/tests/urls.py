# tests/urls.py

from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('<int:mock_test_id>/', views.test_view, name='test_view'),
    path('<int:mock_test_id>/result/', views.result_view, name='result_view'),
]