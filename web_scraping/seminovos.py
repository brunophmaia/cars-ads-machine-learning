from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://seminovos.com.br")

time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
selectBrands = soup.find('select', {"id":"marca"})

brands = map(lambda el: el.get_text().strip(), selectBrands.findChildren())
_listBrands = list(brands)

listBrands = list(filter(lambda x: x != 'Selecione a marca' and x != '-', _listBrands))
listBrands = list(set(listBrands))
listBrands =  list(map(lambda b: b.replace(" ", "-").lower(), listBrands))
listBrands.sort()

yearsRange = [1925, 2000, 2005, 2010, 2012, 2014, 2016, 2018, 2020, 2022]
types = ['origem-particular', 'origem-revenda']

def getAdCar(urlAd, brand, yearStart, yearEnd, _type):
    print(urlAd)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    
    site = requests.get(urlAd, headers=headers)
    soupAd = BeautifulSoup(site.content, 'html.parser')

    divInfos = soupAd.find('div', class_='part-infos')
    
    if(divInfos is None):
        return
    
    divInfosChildren = divInfos.findChildren('div')

    publicacao = divInfosChildren[0].get_text().strip().split(' ')[2]
    codigo = divInfosChildren[2].get_text().strip().split(' ')[1]

    divMarcaModeloValor = soupAd.find('div', class_='part-marca-modelo-valor')
    spanValor = divMarcaModeloValor.find('span', class_='valor') if divMarcaModeloValor is not None else None

    valor = spanValor.get_text().strip().split(' ')[1] if spanValor is not None else None
    motorizacao = divMarcaModeloValor.find('span', class_='desc').get_text().strip().split(' ')[0] if divMarcaModeloValor is not None else None
    marcaModelo = divMarcaModeloValor.find('h1').get_text().strip() if divMarcaModeloValor is not None else None

    divItemsDetalhes = soupAd.find('div', class_='part-items-detalhes-icones')
    items = divItemsDetalhes.find_all('div', class_='item')
    itemsKeys = []
    itemsValues = []

    for item in items:
        itemsKeys.append(item.find('div', class_='campo').get_text().strip())
        itemsValues.append(item.find('span', class_='valor').get_text().strip())

    ulAcessorios = soupAd.find('ul', class_='lista-acessorios')
    itensAcessorios = ulAcessorios.find_all('span', class_='description-print')
    listAcessorios = list(map(lambda el: el.get_text().strip(), itensAcessorios))
    
    cityElement = soupAd.find('address')

    city = cityElement.get_text().strip() if cityElement is not None else None
    
    typeDesc = 'Particular' if _type == 'origem-particular' else 'Profissional'

    row = f'{codigo};{publicacao};{valor};{motorizacao};{marcaModelo};{",".join(itemsKeys)};{",".join(itemsValues)};{",".join(listAcessorios)};{typeDesc};{city}'
        
    with open(f'seminovos_{brand}_{yearStart}_{yearEnd}.csv', 'a', encoding='utf-8') as fp:
        fp.write(row+'\n')

def infiniteScroll(brand, yearStart, yearEnd, _type):
    url = f'https://seminovos.com.br/carro/{brand}/ano-{yearStart}-{yearEnd}/{_type}'
    driver.get(url)
    driver.execute_script('window.scrollTo(0, 0);')
    
    qntCurrent = 0
    qntTotal = 1
    qntScroll = 6000
    previous = qntScroll
    noAd = False

    while qntCurrent < qntTotal:
        previousCurrent = qntCurrent
        time.sleep(3)
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight - 1000);')
        previous += qntScroll

        soup = BeautifulSoup(driver.page_source, "html.parser")
        divTotal = soup.find('div', class_='total-anuncios')
        sectionNoAd = soup.find('section', class_='nenhum-reseultado')
        
        if divTotal is None or sectionNoAd is not None:
            noAd = True
            break;

        strTotal = divTotal.get_text().strip()
        strSplitted = strTotal.split(' ')
        splittedFilter = filter(lambda x: x.isnumeric(), strSplitted)
        listFilter = list(splittedFilter)

        qntCurrent = int (listFilter[0])
        qntTotal = int (listFilter[1])
        
        if previousCurrent == qntCurrent:
            break
    
    if not noAd:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cars = soup.find_all('div', class_='anuncio-thumb-new anuncio-modo-list')
        for car in cars:
            urlAd = car.find_all("a")[0]["href"].split("?")[0]
            url = f'https://seminovos.com.br{urlAd}'
            getAdCar(url, brand, yearStart, yearEnd, _type)

for brand in listBrands:
    for indexYear in range(0, len(yearsRange) - 1):
        for _type in types:
            print(str(yearsRange[indexYear]) + ' - ' + str(yearsRange[indexYear + 1]) + ' - ' + brand)
            infiniteScroll(brand, yearsRange[indexYear], yearsRange[indexYear + 1], _type)

