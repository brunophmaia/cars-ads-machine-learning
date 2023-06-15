import pandas as pd
import re
import os

df_olx = None
df_seminovos = None

def initDataFrames():
    global df_olx
    global df_seminovos

    df_olx = pd.read_csv('step_1_joined_files\\olx_all.csv', sep=';')
    df_olx = df_olx.fillna('')

    df_seminovos = pd.read_csv('step_1_joined_files\\seminovos_all.csv', sep=';')
    df_seminovos = df_seminovos.fillna('')

    df_olx['brand_parsed'] = ''
    df_olx['model_parsed'] = ''
    df_seminovos['brand_parsed'] = ''
    df_seminovos['model_parsed'] = ''

def processCommaIssue():
    for index, row in df_olx.iterrows():
        attrsValues = row['attrs_values']

        attrsValues = attrsValues.replace('Carros, vans e utilitários', 'Carros vans e utilitários')
        attrsValues = attrsValues.replace('2.3 10,8M³(DIE)(E5)', '2.3 10-8M³(DIE)(E5)')
        attrsValues = attrsValues.replace('CARGO 7,5KW (ELÉTRICO)', 'CARGO 7-5KW (ELÉTRICO)')
        attrsValues = attrsValues.replace('CHEVROLET CORVETTE 5.7/ 6.0, 6.2 CONV./STINGRAY', 'CHEVROLET CORVETTE 5.7/ 6.0 6.2 CONV./STINGRAY')

        df_olx.at[index,'attrs_values'] = attrsValues

        if(len(attrsValues.split(',')) > len(row['attrs_keys'].split(','))):
            print(index, row['code'])

def alphaNumChars(str):
    return re.sub('[^A-Za-z0-9]+', '', str).upper()

def getBrandsSeminovosFromFile():
    fileSeminovos = open('brands_models_scraping\\seminovos\\brands.txt', 'r', encoding="utf8")
    lines = fileSeminovos.readlines()
    lineBrandSeminovos = lines[0]
    brandsSeminovos = lineBrandSeminovos.split(",")
    return brandsSeminovos

def brandsModelsSeminovos(rowFile, brandsSeminovos):
    brand_model = rowFile['brand_model']
    
    brand = next(filter(lambda _brand: brand_model.startswith(_brand), brandsSeminovos), None)
    model = None
    
    if(brand is None):
        print(brand_model, rowFile['code'])
        return None
    else:
        model = brand_model.replace(brand, "").strip()
        return {'brand_parsed': alphaNumChars(brand), 'model_parsed': alphaNumChars(model)}
    
def generateDataFrameSeminovos():
    brandsSeminovos = getBrandsSeminovosFromFile()

    for index, rowFile in df_seminovos.iterrows():
        row = brandsModelsSeminovos(rowFile, brandsSeminovos)

        if row is not None:
            df_seminovos.at[index,'brand_parsed'] = row['brand_parsed']
            df_seminovos.at[index,'model_parsed'] = row['model_parsed']

def getBrandsOlxFromFile():
    pathOlxBrandModel = 'brands_models_scraping\\olx'

    dicBrandsModelsOlx = {}

    for file in os.listdir(pathOlxBrandModel):

        brand = file.replace('.txt', "")

        fileBrandOlx = open(f'{pathOlxBrandModel}\\{file}', 'r', encoding="utf8")
        lines = fileBrandOlx.readlines()
        lineModelOlx = lines[0]
        modelsOlx = lineModelOlx.split(",")

        modelsOlx.sort(key=lambda _model: len(_model), reverse=True)

        dicBrandsModelsOlx[brand] = modelsOlx
     
    return dicBrandsModelsOlx
        
def brandsModelsOlx(rowFile, dicBrandsModelsOlx):
    attrs_keys = rowFile['attrs_keys'].split(",")
    attrs_values = rowFile['attrs_values'].split(",")
    
    indexBrand = None
    try:
        indexBrand = attrs_keys.index('Marca')
    except ValueError:
        indexBrand = -1
        
    indexModel = None
    try:
        indexModel = attrs_keys.index('Modelo')
    except ValueError:
        indexModel = -1
    
    if(indexModel < 0 or indexBrand < 0):
        print(f'Indexes Not Fount: {rowFile["code"]}')
        return None
    
    brand = attrs_values[indexBrand]
    model = attrs_values[indexModel]

    brandRemoved = model.replace(brand, "").strip()
    
    modelsInDic = dicBrandsModelsOlx[brand]
    
    modelFound = next(filter(lambda _model: brandRemoved.startswith(_model), modelsInDic), None)
    
    if(modelFound is None):
        return None
        
    return {'brand_parsed': alphaNumChars(brand), 'model_parsed': alphaNumChars(modelFound)}

def generateDataFrameOlx():
    dicBrandsModelsOlx = getBrandsOlxFromFile()
    indexProblems = []
    global df_olx

    for index, rowFile in df_olx.iterrows():
        row = brandsModelsOlx(rowFile, dicBrandsModelsOlx)

        if row is not None:
            df_olx.at[index,'brand_parsed'] = row['brand_parsed']
            df_olx.at[index,'model_parsed'] = row['model_parsed']

            if(row['brand_parsed'] is None or (not row['brand_parsed']) or row['model_parsed'] is None or (not row['model_parsed'])):
                indexProblems.append(index)
        else:
            indexProblems.append(index)
    
    df_olx = df_olx.drop(df_olx.index[indexProblems])

def extractBrandsModelAndSaveFile():
    initDataFrames()
    processCommaIssue()
    generateDataFrameSeminovos()
    generateDataFrameOlx()
    df_olx.to_csv('step_2_brands_models_extracted\\olx.csv', sep=';', encoding='utf-8', index=False)
    df_seminovos.to_csv('step_2_brands_models_extracted\\seminovos.csv', sep=';', encoding='utf-8', index=False)