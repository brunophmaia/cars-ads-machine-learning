import pandas as pd
import os

def getDataFrames(folder):
    df_olx = pd.read_csv(f'{folder}\\olx.csv', sep=';')
    df_olx = df_olx.fillna('')

    df_seminovos = pd.read_csv(f'{folder}\\seminovos.csv', sep=';')
    df_seminovos = df_seminovos.fillna('')

    return df_olx, df_seminovos

def addBrandsSet(df_olx, df_seminovos, setBrandsOlx, setBrandsSeminovos):
    for index, row in df_olx.iterrows():
        setBrandsOlx.add(row['brand_parsed'])

    for index, row in df_seminovos.iterrows():
        setBrandsSeminovos.add(row['brand_parsed'])

def generateDiffsBrands(setBrandsOlx, setBrandsSeminovos):
    olxNotInSeminovos = []
    for brandOlx in setBrandsOlx:
        if brandOlx not in setBrandsSeminovos:
            olxNotInSeminovos.append(brandOlx)

    seminovosNotInOlx = []
    for brandSeminovos in setBrandsSeminovos:
        if brandSeminovos not in setBrandsOlx:
            seminovosNotInOlx.append(brandSeminovos)

    seminovosNotInOlx.sort()
    print('Seminovos Not In Olx:\n')
    print(seminovosNotInOlx)
    olxNotInSeminovos.sort()
    print('\nOlx Not In Seminovos:\n')
    print(olxNotInSeminovos)

def printDiffsBrands(df_olx, df_seminovos):
    setBrandsOlx = set()
    setBrandsSeminovos = set()

    addBrandsSet(df_olx, df_seminovos, setBrandsOlx, setBrandsSeminovos)
    generateDiffsBrands(setBrandsOlx, setBrandsSeminovos)

def renameBrandsSeminovos(df_seminovos, brand, index):
    brandConverted = ''
    match brand:
        case 'VOLKSWAGEN':
             brandConverted = 'VWVOLKSWAGEN'
        case 'CHEVROLET':
             brandConverted = 'GMCHEVROLET'
        case 'WILLYS':
             brandConverted = 'WILLYSOVERLAND'
        case 'KIA':
             brandConverted = 'KIAMOTORS'
        case _:
            brandConverted = brand
            
    df_seminovos.at[index,'brand_parsed'] = brandConverted

def saveDataframes(folder, df_olx, df_seminovos):
    df_olx.to_csv(f'{folder}\\olx.csv', sep=';', encoding='utf-8', index=False)
    df_seminovos.to_csv(f'{folder}\\seminovos.csv', sep=';', encoding='utf-8', index=False)

def renameBrandsAndSaveFile(df_olx, df_seminovos):
    for index, row in df_seminovos.iterrows():
        renameBrandsSeminovos(df_seminovos, row['brand_parsed'], index)

    saveDataframes('step_3_brands_renamed', df_olx, df_seminovos)

def writeFilesDiffs(setAllBrands, dicSeminovos, dicOlx):
    for brand in setAllBrands:
        if brand in dicSeminovos and brand in dicOlx:

            modelsInOlxNotInSeminovos = []
            modelsInSeminovosNotInOlx = []

            for modelOlx in dicOlx[brand]:
                if modelOlx not in dicSeminovos[brand]:
                    modelsInOlxNotInSeminovos.append(modelOlx)

            for modelSeminovos in dicSeminovos[brand]:
                if modelSeminovos not in dicOlx[brand]:
                    modelsInSeminovosNotInOlx.append(modelSeminovos)

            if len(modelsInOlxNotInSeminovos) > 0 and len(modelsInSeminovosNotInOlx) > 0:
                modelsInOlxNotInSeminovos.sort()
                modelsInSeminovosNotInOlx.sort()

                filenameOlx = f'models_diffs\\{brand}\\existsInOlxNotInSeminovos.txt'
                filenameSeminovos = f'models_diffs\\{brand}\\existsInSeminovosNotInOlx.txt'

                os.makedirs(os.path.dirname(filenameOlx), exist_ok=True)
                os.makedirs(os.path.dirname(filenameSeminovos), exist_ok=True)

                with open(filenameOlx, "w") as f:
                    f.write('\n'.join(modelsInOlxNotInSeminovos))

                with open(filenameSeminovos, "w") as f:
                    f.write('\n'.join(modelsInSeminovosNotInOlx))
    
def generateModelsDiffs(df_olx, df_seminovos):
    dicOlx = {}
    dicSeminovos = {}
    setAllBrands = set()

    def addInDic(df, dic, setAllBrands):
        for index, row in df.iterrows():
            brand = row['brand_parsed']
            model = row['model_parsed']
            setAllBrands.add(brand)

            if brand not in dic:
                dic[brand] = set()

            dic[brand].add(model)
            
    addInDic(df_olx, dicOlx, setAllBrands)
    addInDic(df_seminovos, dicSeminovos, setAllBrands)
    writeFilesDiffs(setAllBrands, dicSeminovos, dicOlx)

def renameModelsAndSaveFileSeminovos(df_seminovos):
    
    for index, row in df_seminovos.iterrows():
        brand = row['brand_parsed']
        model = row['model_parsed']

        if 'HATCH' in model and len(model) > 5:
            model = model.replace('HATCH', '')
        if 'SEDAN' in model and len(model) > 5:
            model = model.replace('SEDAN', '')
        if 'CABDUPLA' in model and len(model) > 8:
            model = model.replace('CABDUPLA', '')
        if 'CABSIMPLES' in model and len(model) > 10:
            model = model.replace('CABSIMPLES', '')
        if 'CABEST' in model and len(model) > 6:
            model = model.replace('CABEST', '')

        if(brand == 'BMW' and model == '530I'):
            model = '530IIA'
        if(brand == 'BMW' and model == '1M'):
            model = 'M'
        if(brand == 'CHERY' and model == 'ARRIZO5'):
            model = 'ARRIZO'
        if(brand == 'CHERY' and model == 'ARRIZO6'):
            model = 'ARRIZO'
        if(brand == 'CHRYSLER' and model == '300C'):
            model = '300'
        if(brand == 'CHRYSLER' and model == 'TOWNECOUNTRY'):
            model = 'TOWNCOUNTRY'
        if(brand == 'CITROEN' and model == 'C3PICASSO'):
            model = 'C3'
        if(brand == 'CITROEN' and model == 'C4LOUNGE'):
            model = 'C4'
        if(brand == 'CITROEN' and model == 'C4PALLAS'):
            model = 'C4'
        if(brand == 'CITROEN' and model == 'C4PICASSO'):
            model = 'C4'
        if(brand == 'FIAT' and model == 'FIORINOFURGO'):
            model = 'FIORINO'
        if(brand == 'FIAT' and model == 'PALIOWEEKEND'):
            model = 'PALIO'
        if(brand == 'FIAT' and model == 'SIENAGRAND'):
            model = 'GRANDSIENA'
        if(brand == 'FORD' and model == 'JEEPWILLYS'):
            model = 'JEEP'
        if(brand == 'FORD' and model == 'RANGERCS'):
            model = 'RANGER'
        if(brand == 'FORD' and model == 'RANGERSUPERCAB'):
            model = 'RANGER'
        if(brand == 'HYUNDAI' and model == 'SANTAF'):
            model = 'SANTAFE'
        if(brand == 'LANDROVER' and model == 'DEFENDER110'):
            model = 'DEFENDER'
        if(brand == 'LANDROVER' and model == 'DEFENDER90'):
            model = 'DEFENDER'
        if(brand == 'LANDROVER' and model == 'DISCOVERYSPORT'):
            model = 'DISCOVERY'
        if(brand == 'LEXUS' and model == 'UX'):
            model = 'UX250H'
        if(brand == 'MERCEDESBENZ' and 'SPRINTER' in model):
            model = 'SPRINTER'
        if(brand == 'MERCEDESBENZ' and 'AMG' in model):
            model = model.replace('AMG', '')
        if(brand == 'PEUGEOT' and 'SW' in model):
            model = model.replace('SW', '')
        if(brand == 'PEUGEOT' and 'PASSION' in model):
            model = model.replace('PASSION', '')
        if(brand == 'PEUGEOT' and 'CABRIOLET' in model):
            model = model.replace('CABRIOLET', '')
        if(brand == 'RENAULT' and 'SCNIC' in model):
            model = 'SCENIC'
        if(brand == 'RENAULT' and 'MEGANEGRANDTOUR' in model):
            model = 'MEGANE'
        if(brand == 'TOYOTA' and 'COROLLACROSS' in model):
            model = 'COROLLA'
        if(brand == 'TOYOTA' and 'ETIOSCROSS' in model):
            model = 'ETIOS'
        if(brand == 'TOYOTA' and 'HILUXCD' in model):
            model = 'HILUX'
        if(brand == 'TOYOTA' and 'HILUXCS' in model):
            model = 'HILUX'
        if(brand == 'TOYOTA' and 'HILUXSW4' in model):
            model = 'HILUX'
        if(brand == 'VWVOLKSWAGEN' and 'PASSATVARIANT' in model):
            model = 'PASSAT'
        if(brand == 'WILLYSOVERLAND' and 'OVERLAND' in model):
            model = 'JEEP'

        df_seminovos.at[index,'model_parsed'] = model

    df_seminovos.to_csv('step_4_models_renamed\\seminovos.csv', sep=';', encoding='utf-8', index=False)

def renameModelsAndSaveFileOlx(df_olx):

    for index, row in df_olx.iterrows():
        brand = row['brand_parsed']
        model = row['model_parsed']

        if(brand == 'BMW' and model == '116IA'):
            model = '116I'
        if(brand == 'BMW' and model == '528IA'):
            model = '528I'
        if(brand == 'BMW' and model == '535IA'):
            model = '535I'
        if(brand == 'LANDROVER' and model == 'DISC'):
            model = 'DISCOVERY'
        if(brand == 'LANDROVER' and model == 'EVOQUE'):
            model = 'RANGEROVEREVOQUE'
        if(brand == 'LANDROVER' and model == 'RANGEREVO'):
            model = 'RANGEROVEREVOQUE'
        if(brand == 'LANDROVER' and model == 'EVO'):
            model = 'RANGEROVEREVOQUE'
        if(brand == 'LANDROVER' and model == 'RANGEROVER'):
            model = 'RANGEROVEREVOQUE'
        if(brand == 'LANDROVER' and model == 'RANGERSPORT'):
            model = 'RANGEROVERSPORT'
        if(brand == 'LANDROVER' and model == 'RANGERVE'):
            model = 'RANGEROVERVELAR'
        if(brand == 'LANDROVER' and model == 'RANGERVEL'):
            model = 'RANGEROVERVELAR'
        if(brand == 'LANDROVER' and model == 'RANGERVELAR'):
            model = 'RANGEROVERVELAR'
        if(brand == 'LANDROVER' and model == 'SPORT'):
            model = 'RANGEROVERSPORT'
        if(brand == 'LANDROVER' and model == 'VELAR'):
            model = 'RANGEROVERVELAR'
        if(brand == 'TOYOTA' and model == 'BAND'):
            model = 'BANDEIRANTES'

        df_olx.at[index,'model_parsed'] = model

    df_olx.to_csv('step_4_models_renamed\\olx.csv', sep=';', encoding='utf-8', index=False)

def renameModelsAndSaveFile(df_olx, df_seminovos):
    renameModelsAndSaveFileSeminovos(df_seminovos)
    renameModelsAndSaveFileOlx(df_olx)