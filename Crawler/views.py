from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import ExtractedTerms
from django.http import JsonResponse
from Crawler.get_data import do_ner
class ExtractTerms(APIView):
    def get(self, request, format=None):
        """
        Gets terms.
        """
        results = do_ner()
        for results in results:
            ExtractedTerms.objects.create(Term=results.get("Term",None),Sentence=results.get("Sentence",None),Source=results.get("Source",None))
        return JsonResponse({"success":True})