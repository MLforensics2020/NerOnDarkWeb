from django.db import models
from django.contrib import admin
import datetime 
from django.utils import timezone

# NER Generated Terms.
class ExtractedTerms(models.Model):
    Term = models.TextField(max_length=100,blank=True)
    Sentence = models.TextField(blank=True)
    Source = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    
    def __str__(self):
        return self.Term

# Crawled onion links.
class CrawledOnionLinks(models.Model):
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    
    def __str__(self):
        return self.link

# Input links
class InputLinks(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    visited = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__(self):
        return self.link