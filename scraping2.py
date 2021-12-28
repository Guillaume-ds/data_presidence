import requests as rq
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

analyzer = SentimentIntensityAnalyzer()



headers = {
    'authority': 'www.lemonde.fr',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.lemonde.fr/recherche/?search_keywords=libye&start_at=01%2F01%2F2015&end_at=31%2F12%2F2015&search_sort=relevance_desc',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6'
    }

headersall = {
    'authority': 'www.sueddeutsche.de',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    '$cookie': 'authId=27f834fb-2322-42d3-9972-6af9727925dc; _sp_v1_uid=1:463:2339f406-2322-4699-bc70-7b840c9f734e; _sp_v1_csv=null; _sp_v1_lt=1:; consentUUID=a64ea53c-1382-44d9-9f0a-93e2db9c24eb; _lp4_u=b83MjXtDkN; _sp_enable_dfp_personalized_ads=true; consentStateGoogleAnalytics=true; consentStateGoogleAnalyticsRemarketing=true; consentStateExactag=true; _sp_v1_opt=1:login|true:last_id|11:; iom_consent=0103ff03ff&1625485214357; AMCVS_41833DF75A550B4B0A495DA6%40AdobeOrg=1; s_cc=true; AAMC_iqdigital_0=REGION%7C6; aam_uuid=22856421642167448761159587699127344904; consentStateLinkpulse=false; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbKKhjHySnNydGKUUpHYJWCJ6traWFwSSjqYBhFg5IEYBriNpIcEkrPxeXtglMUCAMo1izmdAQAA; _sp_v1_consent=1\\u00211:1:1:0:0:0; creid=1704446095310182619; _lp4_c=; adbprevpage=/politik/machtkampf-in-aegypten-schweizer-gericht-blockiert-rueckgabe-der-mubarak-millionen-1.1557627; s_sq=%5B%5BB%5D%5D; trc_cookie_storage=taboola%2520global%253Auser-id%3D029df1c3-025a-49f7-91d8-b66738ab9a4b-tuct6635227; _cGtmS=1332654691.1; ioam2018=001d8b9304f75c00b60e2ef98:1652614808288:1625485208288:.sueddeutsche.de:9:sueddeut:spracheDE/formatTXT/erzeugerRED/homepageNO/auslieferungONL/appNO/paidNO/inhaltTHEMA/merkmalNACHRICHTEN/ressortVERMISCHTES/portalSZ:noevent:1625583236642:7ogolv; POPUPCHECK=1625669636643; _gid=GA1.2.1110865732.1625583237; _gat_UA-19474199-5=1; _dc_gtm_UA-19474199-5=1; _k5a=%7B%22u%22%3A%5B%7B%22uid%22%3A%22WtjlfPTePfcpFBxf%22%2C%22ts%22%3A1625583236%7D%2C1625673236%5D%7D; _sp_v1_data=2:362787:1625485208:0:7:0:7:0:0:_:-1; _ga_VCWE23SBVF=GS1.1.1625583236.3.0.1625583236.60; _cGtmAD=1; _ga=GA1.2.687175909.1625485208; emqsegs=e0,e3m,e4y,e38,e8,e3i,e1,e3q,ea,e3o,e3a; adp_segs=e0,e3m,e4y,e38,e8,e3i,e1,e3q,ea,e3o,e3a; AMCV_41833DF75A550B4B0A495DA6%40AdobeOrg=-1124106680%7CMCIDTS%7C18814%7CMCMID%7C22615987812422116061210700522580568498%7CMCAAMLH-1626188037%7C6%7CMCAAMB-1626188037%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1625590437s%7CNONE%7CvVersion%7C5.2.0; adb_dslv=1625583237500',
}

for nb in range(10):
    req = rq.get('https://www.lemonde.fr/recherche/?search_keywords=macron&start_at=01%2F01%2F2012&end_at=31%2F12%2F2021&search_sort=relevance_desc').text
    bsreq = bs(req,'lxml')
    #print(bsreq)
    listea = [a.get('href') for a in bsreq.find_all('a',{'class':'teaser__link'})]
print(listea)


#attention, tous sont des strings sauf le nombre de page et éventuellement l'année ou le mois s'il ne contient qu'une unité et pas de dizaine

def article_lemonde_sentiment(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot,sujet):
    listea = []
    listesent = []
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):
        req = rq.get('https://www.lemonde.fr/recherche/?search_keywords=libye&start_at=01%2F'+str(moisdébut)+'%2F'+str(annéedébut)
                     +'&end_at=31%2F'+str(moisfin)+'%2F'+str(annéefin)+'&search_sort=relevance_desc&page='+str(nb)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'teaser__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        for b in bsreq.find_all('p',{'class':'article__paragraph'}):
            for k in b.strings:
                string+= k
        if mot in string:
            print(string)
            print('\n\n', url, '\n\n')
            listesent.append(float(analyzer.polarity_scores(string)['compound']))
    return(np.mean(listesent))



def article_lemonde(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):
        req = rq.get('https://www.lemonde.fr/recherche/?search_keywords=libye&start_at=01%2F'+str(moisdébut)+'%2F'+str(annéedébut)+'&end_at=31%2F'+str(moisfin)+'%2F'+str(annéefin)+'&search_sort=relevance_desc&page='+str(nb)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'teaser__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        for b in bsreq.find_all('p',{'class':'article__paragraph'}):
            for k in b.strings:
                string+= k
        if mot in string:
            n+= 1
            print(string)
            print('\n\n', url, '\n\n')
           
    return(n)

print(('all' and 'fra') in ('all et frn'))

def article_lemonde_fr(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):
        req = rq.get('https://www.lemonde.fr/recherche/?search_keywords=libye&start_at=01%2F'+str(moisdébut)+'%2F'+str(annéedébut)+'&end_at=31%2F'+str(moisfin)+'%2F'+str(annéefin)+'&search_sort=relevance_desc&page='+str(nb)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'teaser__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        for b in bsreq.find_all('p',{'class':'article__paragraph'}):
            for k in b.strings:
                string+= k
        string1 = string
        string = string.lower()
   
        if mot in string:
            if 'fra' in string:
                print(True)
                n+= 1
                print(string1)
                print('\n\n', url, '\n\n')
           
    return(n)

def article_lemonde_all(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):
        req = rq.get('https://www.lemonde.fr/recherche/?search_keywords=libye&start_at=01%2F'+str(moisdébut)+'%2F'+str(annéedébut)+'&end_at=31%2F'+str(moisfin)+'%2F'+str(annéefin)+'&search_sort=relevance_desc&page='+str(nb)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'teaser__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        for b in bsreq.find_all('p',{'class':'article__paragraph'}):
            for k in b.strings:
                string+= k
        string1 = string
        string = string.lower()
        if mot in string:
            if 'allem' in string:
                print(True)
                n+= 1
                print(string1)
                print('\n\n', url, '\n\n')
           
    return(n)

def graph_sentiment_article_lemonde(annéedébut,annéefin,mot,nombre_de_pages):
    listesentimentarticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listesentimentarticles.append(article_lemonde_sentiment('01',k,12,k, nombre_de_pages, mot))
    print(listesentimentarticles)
    nombremax = max(listesentimentarticles)
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listesentimentarticles)
    plt.title('Vorkommen in Le Monde-Artikeln für das Wort: ' + mot)
    plt.show()



def graph_article_lemonde(annéedébut,annéefin,mot,nombre_de_pages):
    mot = mot.lower()
    print(mot)
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_lemonde('01',k,12,k, nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    listenombrearticles = [k/nombremax*100 for k in listenombrearticles]
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listenombrearticles)
    plt.title('Vorkommen in Le Monde-Artikeln für das Wort: ' + mot)
    plt.show()

def graph_article_lemonde_fr(annéedébut,annéefin,mot,nombre_de_pages):
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_lemonde_fr('01',k,12,k, nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    listenombrearticles = [k/nombremax*100 for k in listenombrearticles]
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listenombrearticles)
    plt.title('Vorkommen in Le Monde-Artikeln für das Wort : ' + mot + 'für Frankreich')
    plt.show()
   
def graph_article_lemonde_all(annéedébut,annéefin,mot,nombre_de_pages):
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_lemonde_all('01',k,12,k, nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    listenombrearticles = [k/nombremax*100 for k in listenombrearticles]
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listenombrearticles)
    plt.title('Vorkommen in Le Monde-Artikeln für das Wort: ' + mot+'für Deutschland')
    plt.show()

def tel_graph_article_lemonde_fr(annéedébut,annéefin,mot,nombre_de_pages,k):
    mot = mot.lower()
    print(mot)
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for a in range(annéedébut,annéefin+1):
        print(a)
        listenombrearticles.append(article_lemonde_fr('01',a,12,a, nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    if nombremax != 0:
        listenombrearticles = [a/nombremax*100 for a in listenombrearticles]
        plt.plot([annéedébut+b for b in range(nombreannées+1)],listenombrearticles)
        plt.title('Vorkommen in Le Monde-Artikeln für das Wort: ' + mot+ ' für Frankreich')
        plt.savefig('/Users/kenzobounegta/Shana pol/'+k+ ' Le monde' +'.png')   # save the figure to file
        plt.close()
   
def tel_graph_article_lemonde_all(annéedébut,annéefin,mot,nombre_de_pages,k):
    mot = mot.lower()
    print(mot)
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for a in range(annéedébut,annéefin+1):
        print(a)
        listenombrearticles.append(article_lemonde_all('01',a,12,a, nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    if nombremax != 0 :
        listenombrearticles = [a/nombremax*100 for a in listenombrearticles]
        plt.plot([annéedébut+b for b in range(nombreannées+1)],listenombrearticles)
        plt.title('Vorkommen in Le Monde-Artikeln für das Wort: ' + mot+' für Deutschland')
        plt.savefig('/Users/kenzobounegta/Shana pol/'+k + 'Le monde' +'.png')
        plt.close()# save the figure to file
   
def article_sueddeutsche(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):

        req = rq.get('https://www.sueddeutsche.de/news?search=Libyen&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&time='+str(annéedébut)+'-' +str(moisdébut) + '-01T00%3A00%2F' +str(annéefin)+'-'+str(moisfin) +  '-01T23%3A59&startDate=01.' + str(moisdébut) +'.' +str(annéedébut)+'&endDate=01.'+str(moisfin) +'.' +str(annéefin)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'entrylist__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        try :
            for b in bsreq.find('div',{'itemprop':'articleBody'}).strings:
                string+= b
            if mot in string:
                n+= 1
                print(string)
                print('\n\n', url, '\n\n')
        except :
            'Ne fonctionne pas pour ' + url
           
    return(n)

def article_sueddeutsche(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):

        req = rq.get('https://www.sueddeutsche.de/news?search=Libyen&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&time='+str(annéedébut)+'-' +str(moisdébut) + '-01T00%3A00%2F' +str(annéefin)+'-'+str(moisfin) +  '-01T23%3A59&startDate=01.' + str(moisdébut) +'.' +str(annéedébut)+'&endDate=01.'+str(moisfin) +'.' +str(annéefin)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'entrylist__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        try :
            for b in bsreq.find('div',{'itemprop':'articleBody'}).strings:
                string+= b
            if mot in string:
                n+= 1
                print(string)
                print('\n\n', url, '\n\n')
        except :
            'Ne fonctionne pas pour ' + url
           
    return(n)

def article_sueddeutsche_fr(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):

        req = rq.get('https://www.sueddeutsche.de/news?search=Libyen&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&time='+str(annéedébut)+'-' +str(moisdébut) + '-01T00%3A00%2F' +str(annéefin)+'-'+str(moisfin) +  '-01T23%3A59&startDate=01.' + str(moisdébut) +'.' +str(annéedébut)+'&endDate=01.'+str(moisfin) +'.' +str(annéefin)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'entrylist__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        try :
            for b in bsreq.find('div',{'itemprop':'articleBody'}).strings:
                string+= b
               
            string1 = string
            string = string.lower()
   
            if mot in string:
                if 'fran' in string:
                    print(True)
                    n+= 1
                    print(string1)
                    print('\n\n', url, '\n\n')
               
        except :
            'Ne fonctionne pas pour ' + url
           
    return(n)

def article_sueddeutsche_all(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):

        req = rq.get('https://www.sueddeutsche.de/news?search=Libyen&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&time='+str(annéedébut)+'-' +str(moisdébut) + '-01T00%3A00%2F' +str(annéefin)+'-'+str(moisfin) +  '-01T23%3A59&startDate=01.' + str(moisdébut) +'.' +str(annéedébut)+'&endDate=01.'+str(moisfin) +'.' +str(annéefin)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'entrylist__link'}):
            listea.append(a.get('href'))

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        try :
            for b in bsreq.find('div',{'itemprop':'articleBody'}).strings:
                string+= b
            string1 = string
            string = string.lower()
   
            if mot in string:
                if 'deuts' in string:
                    print(True)
                    n+= 1
                    print(string1)
                    print('\n\n', url, '\n\n')
               
        except :
            'Ne fonctionne pas pour ' + url
           
    return(n)



def article_sueddeutsche_sentiment(moisdébut,annéedébut,moisfin, annéefin, nombre_de_page, mot):
    listea = []
    listesent = []    
    n = 0
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):

        req = rq.get('https://www.sueddeutsche.de/news?search=Libyen&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&time='+str(annéedébut)+'-' +str(moisdébut) + '-01T00%3A00%2F' +str(annéefin)+'-'+str(moisfin) +  '-01T23%3A59&startDate=01.' + str(moisdébut) +'.' +str(annéedébut)+'&endDate=01.'+str(moisfin) +'.' +str(annéefin)).text
        bsreq = bs(req,'lxml')
        #print(bsreq)
        for a in bsreq.find_all('a',{'class':'entrylist__link'}):
            listea.append(a.get('href'))
    print(listea)

    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        try :
            for b in bsreq.find('div',{'itemprop':'articleBody'}).strings:
                string+= b
            if mot in string:
                n+= 1
                print(string)
                print('\n\n', url, '\n\n')
                print('\n\n', float(analyzer.polarity_scores(string)['compound']),'\n\n')
                listesent.append(float(analyzer.polarity_scores(string)['compound']))
        except :
            'Ne fonctionne pas pour ' + url
           
    return(np.mean(listesent))


def graph_article_sueddeutsche(annéedébut,annéefin,mot,nombre_de_pages):
   
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_sueddeutsche('01',str(k),'12',str(k), nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    listenombrearticles = [k/nombremax*100 for k in listenombrearticles]
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listenombrearticles)
    plt.title('Vorkommen in Sueddeutsche-Artikeln für das Wort: ' + mot)
    plt.show()
   
def tel_graph_article_sueddeutsche_fr(annéedébut,annéefin,mot,nombre_de_pages):
   
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_sueddeutsche_fr('01',str(k),'12',str(k), nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    if nombremax != 0 :
        listenombrearticles = [a/nombremax*100 for a in listenombrearticles]
        plt.plot([annéedébut+b for b in range(nombreannées+1)],listenombrearticles)
        plt.title('Vorkommen in Le Sueddeutsche-Artikeln für das Wort: ' + mot+' für Frankreich')
        plt.savefig('/Users/kenzobounegta/Shana pol/Suedde'+ mot + '-Sueddeutsche' +'.png')
        plt.close()# save the figure to file

def tel_graph_article_sueddeutsche_all(annéedébut,annéefin,mot,nombre_de_pages):
    mot = mot.lower()
    listenombrearticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listenombrearticles.append(article_sueddeutsche_all('01',str(k),'12',str(k), nombre_de_pages, mot))
    print(listenombrearticles)
    nombremax = max(listenombrearticles)
    if nombremax != 0 :
        listenombrearticles = [a/nombremax*100 for a in listenombrearticles]
        plt.plot([annéedébut+b for b in range(nombreannées+1)],listenombrearticles)
        plt.title('Vorkommen in Le Sueddeutsche-Artikeln für das Wort: ' + mot+' für Deutschland')
        plt.savefig('/Users/kenzobounegta/Shana pol/Suedde'+ mot + '-Sueddeutsche' +'.png')
        plt.close()# save the figure to file
   
   
def graph_sentiment_article_sueddeutsche(annéedébut,annéefin,mot,nombre_de_pages):
    listesentimentarticles = []
    nombreannées = annéefin-annéedébut
    print(nombreannées)
    for k in range(annéedébut,annéefin+1):
        print(k)
        listesentimentarticles.append(article_sueddeutsche_sentiment('01',str(k),'12',str(k), nombre_de_pages, mot))
    print(listesentimentarticles)
    nombremax = max(listesentimentarticles)
    plt.plot([annéedébut+a for a in range(nombreannées+1)],listesentimentarticles)
    plt.title('Gefühle in Sueddeutsche-Artikeln für das Wort: ' + mot)
    plt.show()

listeallemand = ['Teilnahme','Internationale Organisationen','UNHCR', 'UNO', 'Multilaterale', 'Kooperation', 'Meinung der Bevölkerung', 'Partizipation der Bevölkerung',  'Humanitäre Intervention', 'gewaltfrei', 'friedlich', 'gewaltlos', 'ohne Gewalt', 'Solidarität','Militär Intervention', 'Konflikt', 'Konfliktlösung', 'Armee', 'Gewalt','Interdependenz']
'militär','frieden','stabilität'

listefrancais = ['Autonomie', 'Selbstständigkeit','Aktivismus','Tätigkeit', 'Handeln','Initiative','Präsenz','Beteiligung', 'Teilnahme','Europa als Macht','Europa', 'Europäische Union','Deutsch-Französisch', 'Frieden', 'Stabilität', 'Stabilitätsgarant']

tel_graph_article_sueddeutsche_all(2011, 2021, 'frieden',3)
tel_graph_article_sueddeutsche_all(2011, 2021, 'stabilität',3)

for motfra in listefrancais :
    print(motfra)
    tel_graph_article_sueddeutsche_fr(2011,2021,motfra,3)


for motfra in listeallemand:
    print(motfra)
    tel_graph_article_sueddeutsche_all(2011,2021,motfra,3)


graph_article_lemonde_all(2011, 2021, 'opinion publique', 10)