import numpy as np
import pandas as pd
import random

def getDataFrameJoined(folder):
    df = pd.read_csv(f'{folder}\\ads.csv', sep=';')
    df = df.fillna('')

    return df

def separate_brand_model(df):

    brands = []

    for index, row in df.iterrows():
        brand = row['brand_parsed']
        model = row['model_parsed']

        brandFound = None

        for _brand in brands:
            if(_brand['brand'] == brand):
                brandFound = _brand
        
        if brandFound is None:
            brandFound = {'brand': brand, 'models': []}
            brands.append(brandFound)

        insert_in_brand(brandFound['models'], model, row)
        
    return brands

        
def insert_in_brand(models, model, row):

    modelFound = None

    for _model in models:
        if(_model['model'] == model):
            modelFound = _model
    
    if modelFound is None:
        modelFound = {'model': model, 'ads': []}
        models.append(modelFound)
    
    modelFound['ads'].append(row)


def fill_cat_values(df, key):

    brands = separate_brand_model(df)
    
    for index, row in df.iterrows():
        if row[key] == '':
            dic_values = {}
            dic_values_not_year = {}

            for _brand in brands:
                if _brand['brand'] == row['brand_parsed']:
                    for _model in _brand['models']:
                        if _model['model'] == row['model_parsed']:
                            for ad in _model['ads']:
                                getValues(dic_values, dic_values_not_year, row, ad, key)

            values = []
            weights = []

            dic_values = dic_values if len(dic_values) > 0 else dic_values_not_year

            for valueCount in dic_values:
                values.append(valueCount)
                weights.append(dic_values[valueCount])

            chosenValue = ''
            if len(values) > 0:
                chosenValue = random.choices(values, weights, k=1)[0]

            df.at[index,key] = chosenValue
    
def getValues(dic_values, dic_values_not_year, row, _row, key):

    if _row[key] != '' and _row['brand_parsed'] == row['brand_parsed'] and _row['model_parsed'] == row['model_parsed']:

        if _row['ano'] == row['ano']:
            if (_row[key] not in dic_values):
                dic_values[_row[key]] = 1
            else:
                dic_values[_row[key]] += 1

        if (_row[key] not in dic_values_not_year):
            dic_values_not_year[_row[key]] = 1
        else:
            dic_values_not_year[_row[key]] += 1

def fill_val_values(df, key, raw_key):

    brands = separate_brand_model(df)
    
    for index, row in df.iterrows():

        if row[key] == '' or int(row[key]) == 0:

            year = int(row['ano'])
            value = ''
            
            while year <= 2022:

                average_values_obj = {
                    'sum_year': 0,
                    'count_year': 0
                }

                for _brand in brands:
                    if _brand['brand'] == row['brand_parsed']:
                        for _model in _brand['models']:
                            if _model['model'] == row['model_parsed']:
                                for ad in _model['ads']:
                                    average_values_obj = sum_value_and_count_values(average_values_obj, row, ad, key, year, raw_key)

                if average_values_obj['count_year'] > 0:
                    value = df.at[index,key] = int(round(average_values_obj['sum_year'] / average_values_obj['count_year']))
                    break
                    
                year += 1

            df.at[index,key] = value

            if value != '':
                df.at[index,f'{raw_key}_outlier'] = 'NÃO'

def sum_value_and_count_values(average_values_obj, row, ad, key, year, raw_key):
    if ad[key] != '' and int(ad[key]) != 0 and ad['ano'] == year and  ad['brand_parsed'] == row['brand_parsed'] and ad['model_parsed'] == row['model_parsed'] and ad[f'{raw_key}_outlier'] != 'TALVEZ' and ad[f'{raw_key}_outlier'] != 'AMOSTRA PEQUENA':
        average_values_obj['sum_year'] += int(ad[key])
        average_values_obj['count_year'] += 1

    return average_values_obj


def fill_category_missing_values(df):

    category_keys = ['portas', 'cambio', 'direcao', 'combustivel', 'motorizacao', 'cor']

    for cat_key in category_keys:
        print(cat_key)
        fill_cat_values(df, cat_key)

def fill_value_missing_values(df):

    values_key = ['price', 'quilometragem']

    for val_key in values_key:
        print(val_key)
        fill_val_values(df, f'{val_key}_processed', val_key)


def outliers(df):

    values_key = ['price', 'quilometragem']

    for val_key in values_key:
        for index, row in df.iterrows():
            
            if(row[val_key] != ''):

                intval = int(row[val_key])

                if intval <= 1000:
                    df.at[index, val_key] = ''

    brands = separate_brand_model(df)

    for val_key in values_key:

        df[f'{val_key}_processed'] = ''
        df[f'{val_key}_outlier'] = ''

        outliers_by_key(val_key, df, brands)

def outliers_by_key(key, df, brands):

    TAMANHO_AMOSTRA = 3

    for index, row in df.iterrows():
        if row[key] == '':
            continue

        year = int(row['ano'])

        values = []

        while year <= 2022:

            for _brand in brands:
                if _brand['brand'] == row['brand_parsed']:
                    for _model in _brand['models']:
                        if _model['model'] == row['model_parsed']:
                            for ad in _model['ads']:
                                if ad[key] != '' and  int(ad[key]) != 0 and ad['ano'] == year:
                                    values.append(int(ad[key]))
            
            if len(values) > TAMANHO_AMOSTRA:
                break

            year += 1

        valKey = int(row[key])

        if len(values) > 1:
            fator = 1.5
            q3, q1 = np.percentile(values, [75, 25])
            iqr = q3 - q1
            lowpass = q1 - (iqr * fator)
            highpass = q3 + (iqr * fator)

            if valKey < lowpass or valKey > highpass:
                df.at[index,f'{key}_processed'] = round((q3 + q1)/2)
                df.at[index,f'{key}_outlier'] = 'CORRIGIDO'
            else:
                df.at[index,f'{key}_processed'] = valKey
                df.at[index,f'{key}_outlier'] = 'AMOSTRA PEQUENA' if len(values) <= TAMANHO_AMOSTRA else 'NÃO'
        else: 
            df.at[index,f'{key}_processed'] = valKey
            df.at[index,f'{key}_outlier'] = 'TALVEZ'


def delete_missing_cities(df):

    no_city = []

    for index, row in df.iterrows():
        if row['city_processed'] == '':
            no_city.append(index)

    df = df.drop(df.index[no_city])

    return df

def write_csv(df):
    df.to_csv('step_6_etl_done\\ads.csv', sep=';', encoding='utf-8', index=False)