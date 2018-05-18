#! env python3

# -*- coding: utf-8 -*-
# Скрипт выкачивания ссылок на статьи с elibrary.ru

# http://elibrary.ru/item.asp?id=30574807


import requests
import io

from lxml import html
from lxml import etree



class Article:
    """ Класс для описания одной статьи """
    def __init__(self):
        self.title=''
        self.authors=[]
        self.keywords=[]
        self.year=0
        self.annotation=''
        pass

    def __str__(self):
        s=""
        s+="Статья: "+ self.title+"\n"
        #s+="Авторы: "+ ', '.join(self.authors)+"\n"
        #s+="Ключевые слова: "+ ', '.join(self.keywords)+"\n"
        #s+="Год: "+ str(self.year)+"\n"
        #s+="Аннотация: "+self.annotation+"\n"
        return s



class ElibraryDownloader:
    """ Скачивалка статей с elibrary.ru """
    title_xpath  ='/html/body/table/tr/td/table[1]/tr/td[2]/table/tr[2]/td[1]/table/tr/td[2]/span/span/b'
    authors_xpath='/html/body/table/tr/td/table[1]/tr/td[2]/table/tr[2]/td[1]/div/table[1]/tr/td[2]/span'
    kw_xpath='/html/body/table/tr/td/table[1]/tr/td[2]/table/tr[2]/td[1]/div/table[4]/tr[2]/td[2]/a'
    year_xpath='/html/body/table/tr/td/table[1]/tr/td[2]/table/tr[2]/td[1]/div/table[2]/tr[3]/td/font[2]'
    annot_xpath='/html/body/table/tr/td/table[1]/tr/td[2]/table/tr[2]/td[1]/div/table[5]/tr[2]/td[2]/p'

    def __init__(self):
        self.ps = requests.Session()
        self.ps.headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        self.parser = etree.HTMLParser()

    def ParseHTML(self,s):
        r = Article()
        t = etree.parse(io.StringIO(s), self.parser)
        
        r.title=t.xpath(self.title_xpath)[0].text

        authlist=t.xpath(self.authors_xpath)
        for ai in authlist:
            r.authors.append(ai[0][0].text)

        kwlist=t.xpath(self.kw_xpath)
        for kwi in kwlist:
            r.keywords.append(kwi.text)

        r.year=t.xpath(self.year_xpath)[0].text

        ai=t.xpath(self.annot_xpath)
        for at in ai :
            r.annotation+=at.text+"\n"

        return r

    def GetArticle(self,id):

        url = 'http://elibrary.ru/item.asp?id='+str(id)
        r=self.ps.get(url)

        return self.ParseHTML(r.text)
        

def Main():

    dl=ElibraryDownloader()

    ids=[30574806, 30574807, 30574808, 30574809, 30574810]

    #for id in ids :
    for id in range(30574810, 30575000) :
        try:
            bib=dl.GetArticle(id)
            print(bib)
        except Exception:
            print("id:", id," ERROR")

    return



if __name__ == "__main__":
    # execute only if run as a script
    Main()


