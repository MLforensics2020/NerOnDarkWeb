from django.contrib import admin
from django.urls import path
from .views import ExtractTerms

urlpatterns = [
    path('get_terms/', ExtractTerms.as_view()),
]