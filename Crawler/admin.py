from django.contrib import admin
from .models import ExtractedTerms , CrawledOnionLinks
# Register your models here.

class ExtractedTermsAdmin(admin.ModelAdmin):
    model = ExtractedTerms
    fields = ('Term', 'Sentence','Source')
    list_filter = ('Source',)
    ordering = ['updated_at']
    search_fields = ['Term', 'Sentence','Source']

class CrawledOnionLinksAdmin(admin.ModelAdmin):
    model = CrawledOnionLinks
    fields = ('link',)
    list_filter = ('updated_at',)
    ordering = ['updated_at']
    search_fields = ['link']

admin.site.register(ExtractedTerms,ExtractedTermsAdmin)
admin.site.register(CrawledOnionLinks,CrawledOnionLinksAdmin)