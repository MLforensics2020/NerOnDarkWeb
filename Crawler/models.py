from django.db import models
from django.contrib import admin
import datetime 
from django.utils import timezone
# Create your models here.
class ExtractedTerms(models.Model):
    Term = models.TextField(max_length=100,blank=True)
    Sentence = models.TextField(blank=True)
    Source = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    
    def __str__(self):
        return self.Term
