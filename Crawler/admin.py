from django.contrib import admin
from .models import ExtractedTerms
# Register your models here.

class ExtractedTermsAdmin(admin.ModelAdmin):
    model = ExtractedTerms
    fields = ('Term', 'Sentence','Source')
    list_filter = ('Source',)
    ordering = ['updated_at']
    search_fields = ['Term', 'Sentence','Source']
admin.site.register(ExtractedTerms,ExtractedTermsAdmin)