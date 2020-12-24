from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import ExtractedTerms , CrawledOnionLinks
from django.http import JsonResponse
from Crawler.get_data import do_ner
from Crawler.torcrawl import main

class ExtractTerms(APIView):
    def get(self, request, format=None):
        """
        Gets terms.
        """
        results = do_ner()
        for result in results:
            ExtractedTerms.objects.create(Term=results.get("Term",None),Sentence=results.get("Sentence",None),Source=results.get("Source",None))
        return JsonResponse({"success":True})

class RunCrawler(APIView):
    def alreadyExists(self,link):
        return CrawledOnionLinks.objects.filter(link=link).exists()
    
    def get(self, request, format=None):
        """
        Gets links, html.
        """
        links = main()
        queries = list()
        for link in links:
            if self.alreadyExists(link) :
                pass
            else:
                queries.append(CrawledOnionLinks(link=link))
        CrawledOnionLinks.objects.bulk_create(queries)
        return JsonResponse({"success":True,"links":links})