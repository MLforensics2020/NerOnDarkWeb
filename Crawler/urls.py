from django.contrib import admin
from django.urls import path
from .views import ExtractTerms,RunCrawler,Add_Onion_File

urlpatterns = [
    path('get_terms/', ExtractTerms.as_view()),
    path('run_crawler/', RunCrawler.as_view()),
    path('add-onion-file/', Add_Onion_File.as_view()),
]