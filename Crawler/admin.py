from django.contrib import admin
from .models import ExtractedTerms , CrawledOnionLinks , InputLinks
# Register your models here.

class ExtractedTermsAdmin(admin.ModelAdmin):
    model = ExtractedTerms
    fields = ('Term', 'Sentence','Source')
    list_filter = ('Source',)
    ordering = ['updated_at']
    search_fields = ['Term', 'Sentence','Source']
    list_display = ('Term', 'Sentence','Source','updated_at')

class CrawledOnionLinksAdmin(admin.ModelAdmin):
    model = CrawledOnionLinks
    fields = ('link',)
    list_filter = ('updated_at',)
    ordering = ['updated_at']
    search_fields = ['link']

class InputLinksAdmin(admin.ModelAdmin):
    change_list_template = 'change_list.html'
    model = InputLinks
    fields = ('name','link','visited')
    list_filter = ('visited',)
    ordering = ['created_at']
    search_fields = ['name','link']
    list_display = ('name','link','visited','created_at')

admin.site.register(ExtractedTerms,ExtractedTermsAdmin)
admin.site.register(CrawledOnionLinks,CrawledOnionLinksAdmin)
admin.site.register(InputLinks,InputLinksAdmin)