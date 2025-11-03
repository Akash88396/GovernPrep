
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('test/', include('tests.urls')),
    path('my-test-series/', include('test_series.urls')),
    path('', include('exams.urls')),

]
