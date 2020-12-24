from django.contrib import admin
from django.urls import path
from .views import ExtractTerms,RunCrawler

urlpatterns = [
    path('get_terms/', ExtractTerms.as_view()),
    path('run_crawler/', RunCrawler.as_view()),
]