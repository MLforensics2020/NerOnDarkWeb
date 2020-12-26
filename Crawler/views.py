from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import ExtractedTerms , CrawledOnionLinks , InputLinks
from django.http import JsonResponse
from Crawler.get_data import do_ner
from Crawler.torcrawl import crawl
from Crawler.utils import chunk
class ExtractTerms(APIView):
    def get(self, request, format=None):
        """
        Gets terms.
        """
        results = do_ner()
        for result in results:
            ExtractedTerms.objects.create(Term=result.get("Term",None),Sentence=result.get("Sentence",None),Source=result.get("Source",None))
        return JsonResponse({"success":True})

class RunCrawler(APIView):
    def alreadyExists(self,link):
        return CrawledOnionLinks.objects.filter(link=link).exists()
    
    def get(self, request, format=None):
        """
        Gets links, html.
        """
        unvisitedLinks = InputLinks.objects.filter(visited=False).values_list('link',flat=True)
        chunksOfUnvisitedLinks = list(chunk(unvisitedLinks, 10))
        for urlChunk in chunksOfUnvisitedLinks:
            queries = list()
            links = crawl(list(urlChunk))
            for link in links:
                if self.alreadyExists(link) :
                    print("Already exists")
                else:
                    queries.append(CrawledOnionLinks(link=link))
            for url in urlChunk:
                a = InputLinks.objects.get(link=url)
                a.visited = True
                a.save()
            CrawledOnionLinks.objects.bulk_create(queries)
        return JsonResponse({"success":True})
