import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

regions = ['belo-horizonte-e-regiao','regiao-de-juiz-de-fora',
           'regiao-de-governador-valadares-e-teofilo-otoni',
           'regiao-de-uberlandia-e-uberaba',
           'regiao-de-pocos-de-caldas-e-varginha',
           'regiao-de-divinopolis',
           'regiao-de-montes-claros-e-diamantina']

types = ['c','p']
startYear = 1990
endYear = 2022
years = [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985]
for i in range (startYear, endYear + 1):
    years.append(i)

def getAd(urlAd, region, year, _type):
    site = requests.get(urlAd, headers=headers)
    soupAdd = BeautifulSoup(site.content, 'html.parser')

    publishDateElement = soupAdd.find('span', class_='ad__sc-1oq8jzc-0 hSZkck sc-ifAKCX fizSrB')
    publishDate = publishDateElement.get_text().strip() if publishDateElement is not None else None
    
    codeElement = soupAdd.find('span', class_='ad__sc-16iz3i7-0 bTSFxO sc-ifAKCX fizSrB')
    code = codeElement.get_text().strip() if codeElement is not None else None
    
    priceElement = soupAdd.find('h2', class_='ad__sc-12l420o-1 cuGsvO sc-drMfKT fbofhg')
    price = priceElement.get_text().strip() if priceElement is not None else None
    
    diffsElements = map(lambda el: el.get_text().strip(), soupAdd.find_all('span', class_='info sc-iqzUVk leQbaP'))
    diffsList = list(diffsElements)

    divParentSpecs = soupAdd.find('div', class_='sc-hmzhuo ad__sc-1g2w54p-1 liYUIw sc-jTzLTM iwtnNi')
    divSpecs =  divParentSpecs.find('div', class_='sc-bwzfXH ad__h3us20-0 ikHgMx') if divParentSpecs is not None else None
    specsElements = divSpecs.find_all('div', {"class":"sc-hmzhuo ccYVdB sc-jTzLTM iwtnNi"}) if divSpecs is not None else []

    specsdict = {}

    for specElement in specsElements:
        childs = specElement.findChildren()
        keySpec = childs[0].get_text().strip()
        valueSpec = childs[1].get_text().strip()
        specsdict.update({keySpec: valueSpec})


    divExtras = soupAdd.find('div', class_='sc-bwzfXH ad__h3us20-0 cyymIl')
    divsExtras = []
    
    if(divExtras is not None):
        divsExtras = divExtras.find_all('span', class_='ad__sc-1g2w54p-0 eDzIHZ sc-ifAKCX cmFKIN')
    
    extrasElements = map(lambda el: el.get_text().strip(), divsExtras)
    extrasList = list(extrasElements)

    divLocalParent = soupAdd.find('div', class_='ad__h3us20-6 crHfst')
    divLocal = divLocalParent.find('div', class_='sc-bwzfXH ad__h3us20-0 ikHgMx') if divLocalParent is not None else None
    divsItemsLocal = divLocal.find_all('div', {"class":"ad__duvuxf-0 ad__h3us20-0 kUfvdA"}) if divLocal is not None else []    
    divCity = divsItemsLocal[1] if len(divsItemsLocal) > 1 else None
    city = divCity.find('dd', class_='ad__sc-1f2ug0x-1 cpGpXB sc-ifAKCX kaNiaQ').get_text().strip() if divCity is not None else None
    
    typeDesc = 'Particular' if _type == 'p' else 'Profissional' 

    keys = []
    values = []

    for key in specsdict:
        keys.append(key)
        values.append(specsdict.get(key))

    row = f'{publishDate};{code};{price};{",".join(diffsList)};{",".join(values)};{",".join(keys)};{",".join(extrasList)};{typeDesc};{city};{urlAd}'

    with open(f'cars_{region}_{year}.csv', 'a', encoding='utf-8') as fp:
        fp.write(row+'\n')
    
def countPages(url):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    count_itemsStr = soup.find('span', class_='sc-1mi5vq6-0 dQbOE sc-ifAKCX fCbscF').get_text().strip()
    count_items = int (count_itemsStr.split(' ')[4].replace('.',''))
    count_pages = math.ceil(count_items / 50)
    return count_pages

def getCars(_countPage, region, year, _type):
    for i in range(1, _countPage + 1):
        print(_countPage, i, region, year, _type)
        url_pag =  f'https://mg.olx.com.br/{region}/autos-e-pecas/carros-vans-e-utilitarios/{year}?f={_type}&o={i}'
        site = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        cars = soup.find_all('a', {"class":"sc-12rk7z2-1 huFwya sc-htoDjs fpYhGm"})
        for car in cars:
            time.sleep(1)
            getAd(car['href'], region, year, _type)

for region in regions:
    for year in years:
        for _type in types:
            url = f'https://mg.olx.com.br/{region}/autos-e-pecas/carros-vans-e-utilitarios/{year}?f={_type}'
            getCars(countPages(url), region, year, _type)