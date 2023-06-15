from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import warnings
warnings.filterwarnings('ignore')



def getBrandsScrapingSeminovos():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://seminovos.com.br")

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    selectBrandsSeminovos = soup.find('select', {"id":"marca"})

    brandsSeminovos = map(lambda el: el.get_text().strip(), selectBrandsSeminovos.findChildren())
    _listBrandsSeminovos = list(brandsSeminovos)

    listBrandsSeminovos = list(filter(lambda x: x != 'Selecione a marca' and x != '-', _listBrandsSeminovos))
    listBrandsSeminovos = list(set(listBrandsSeminovos))

    with open('brands_models_scraping\\seminovos\\brands.txt', 'a', encoding='utf-8') as fp:
                fp.write(",".join(listBrandsSeminovos))

def getBrandsScrapingOlx():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    selectBrandsOlx = soup.find('select', {"class":"g98wuw-1 hpeKug"})

    brandsOlx = map(lambda el: el.get_text().strip(), selectBrandsOlx.findChildren())
    _listBrandsOlx = list(brandsOlx)

    listBrandsOlx = list(filter(lambda x: x != 'Marca', _listBrandsOlx))
    listBrandsOlx = list(set(listBrandsOlx))

    xpathBrand = '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[1]/div[1]/div/div/div/select'

    selectBrand = Select(driver.find_element(By.XPATH, xpathBrand))

    for brand in listBrandsOlx:
        selectBrand.select_by_visible_text(brand)
        time.sleep(3)
        
        soupModel = BeautifulSoup(driver.page_source, "html.parser")
        selectModel = soupModel.find_all('select', {"class":"g98wuw-1 hpeKug"})
        
        modelsOlx = map(lambda el: el.get_text().strip(), selectModel[1].findChildren())
        _listModelsOlx = list(modelsOlx)
        
        listModelsOlx = list(filter(lambda x: x != 'Modelo', _listModelsOlx))
        listModelsOlx = list(set(listModelsOlx))
        
        with open(f'brands_models_scraping\\olx\\{brand}.txt', 'a', encoding='utf-8') as fp:
            fp.write(",".join(listModelsOlx))
        
        selectBrand = Select(driver.find_element(By.XPATH, xpathBrand))

def executeCombosScraping():
    getBrandsScrapingSeminovos()
    getBrandsScrapingOlx()