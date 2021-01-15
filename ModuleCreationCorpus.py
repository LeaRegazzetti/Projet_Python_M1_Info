#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################### Création du Corpus ######################################
import urllib.request
import xmltodict   
import pandas
import ModuleCorpus as MC
import datetime as dt

#Fonction permettant la création d'un corpus en lien avec le thème entré par l'utilisateur
def Creation(thm):

    corpus = MC.Corpus(thm)

    url = 'http://export.arxiv.org/api/query?search_query=all:'+str(thm)+'&start=0&max_results=100'
    data =  urllib.request.urlopen(url).read().decode()
    docs = xmltodict.parse(data)['feed']['entry']
    
    lst_titres=[]
    sources=[]
    targets=[]
    for i in docs:
        datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            author = [aut['name'] for aut in i['author']][0]
        except:
            author = i['author']['name']
        txt = i['summary']
        titre=i['title']
        doc = MC.Document(datet,
               i['title'],
               author,
               txt,
               i['id']
               )
        clear_txt = doc.nettoyer_texte(txt)
        doc_clear = MC.Document(datet,
               titre,
               author,
               clear_txt,
               i['id']
               )
        #Création du vocabulaire, à savoir la liste des mots
        vocab=doc_clear.voca(clear_txt)
        corpus.add_doc(doc_clear)

    
        #Création d'une liste contenant les titres des documents pour l'interface
        lst_titres.append(titre)  
        
        #Ajout du vocabulaire dans des listes pour les graphes
        sources.append(vocab[0:len(vocab)-1])
        targets.append(vocab[1:len(vocab)])

    #Création d'une liste de dataframe contenant les mots pour chaque document pour les graphes
    liste_document=[]
    for i in range(len(sources)):
        liste_document.append([])
        liste_document[i]=pandas.DataFrame()
        liste_document[i]['source'] = pandas.Series(sources[i])
        liste_document[i]['target'] = pandas.Series(targets[i])
    
    return lst_titres, liste_document
