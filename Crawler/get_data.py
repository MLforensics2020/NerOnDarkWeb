import os
import codecs 
import requests,csv
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
from collections import Counter
"""PERSON	People, including fictional.
NORP	Nationalities or religious or political groups.
FAC	Buildings, airports, highways, bridges, etc.
ORG	Companies, agencies, institutions, etc.
GPE	Countries, cities, states.
LOC	Non-GPE locations, mountain ranges, bodies of water.
PRODUCT	Objects, vehicles, foods, etc. (Not services.)
EVENT	Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART	Titles of books, songs, etc.
LAW	Named documents made into laws.
LANGUAGE	Any named language.
DATE	Absolute or relative dates or periods.
TIME	Times smaller than a day.
PERCENT	Percentage, including ”%“.
MONEY	Monetary values, including unit.
QUANTITY	Measurements, as of weight or distance.
ORDINAL	“first”, “second”, etc.
CARDINAL	Numerals that do not fall under another type."""
def do_ner():
    import en_core_web_sm
    nlp = spacy.load('en_core_web_sm')
    SOURCE_FOLDER = "Crawler/source_pages"
    files = [f for f in os.listdir(SOURCE_FOLDER)]
    #   if os.path.isfile(f) and f!='get_data.ipynb']
    print(files)
    person_dict={'PERSON':[],'sentence':[],'page_where_occured':[]}
    finalResult = []
    for p in files :
        #print(p)
        page= codecs.open('{}/{}'.format(SOURCE_FOLDER,p),'r')
        page=page.read()
        soup = BeautifulSoup(page, 'html.parser')
        page = "".join([p.text for p in soup.find_all("p")])
        article = nlp(page)
        labels = [x.label_ for x in article.ents]
        Counter(labels)
        items = [x.text for x in article.ents]
        sentences = [x for x in article.sents]
        # print("sentences",sentences)
        for sentence in sentences :
            current_sentence=sentence
            for x in current_sentence:
                if x.ent_type_=='PERSON' :
                    person_dict = dict()
                    person_dict['Term'] = str(x)
                    person_dict['Sentence'] = str(sentence)
                    person_dict['Source'] = str(p)
                    finalResult.append(person_dict)
        #print(len(person_dict['PERSON']))
        # print(person_dict['PERSON'])
    # for name in person_dict['PERSON']:
    #     if name.text.lower()=='mediolanum':
    #         print('mediolanum found')
    print("finalResult",finalResult)
    # keys = finalResult[0].keys()
    # with open('results.csv', 'w', newline='') as csv_file:  
    #     dict_writer = csv.DictWriter(csv_file,keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(finalResult)
    return finalResult