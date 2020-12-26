from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import ExtractedTerms , CrawledOnionLinks , InputLinks
from django.http import JsonResponse
from Crawler.get_data import do_ner
from Crawler.torcrawl import crawl
import csv, io
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from Crawler.utils import chunk

class ExtractTerms(APIView):
    def get(self, request, format=None):
        """
        Gets terms.
        """
        results = do_ner()
        for result in results:
            try:
                ExtractedTerms.objects.create(Term=result.get("Term",None),Sentence=result.get("Sentence",None),Source=result.get("Source",None))
            except Exception as e:
                print("Exception while saving term => ",e)
        return JsonResponse({"success":True})

@method_decorator(csrf_exempt, name='dispatch')
class Add_Onion_File(APIView):
    def post(self, request, format=None):
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"success":False,"message":'THIS IS NOT A CSV FILE'})
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            InputLinks.objects.create(
                name=column[0],
                link=column[1],
                visited=False
            )
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
