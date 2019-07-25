import spacy
from nltk.corpus import wordnet
import re

def extractName(string):
    list_words = string.split()
    count = len(list_words)
    if count > 4:
        return False
    for each in list_words:
        if wordnet.synsets(each):
            return False
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~]')
    if regex.search(string) != None:
        return False
    if string.isupper():
        string = string.title()
    r1 = str(string)
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(r1)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            return True
    return False

def extractPhone(string):
    regex = re.compile('\S+@\S+')
    if regex.search(string) != None:
        return True
    return False

def extractEmail(string):
    regex = re.compile('.*\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}.*')
    if regex.search(string) != None:
        return True
    return False