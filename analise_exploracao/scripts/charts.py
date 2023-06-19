from scripts.common import get_dataframe

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def days_ad():
    df = get_dataframe()
    
    countlower1 = 0
    count1_7 = 0
    count7_30 = 0
    countgreater30 = 0

    for index, row in df.iterrows():

        days = int(row['posted_days'])

        if(days == 0):
            countlower1 += 1
        elif(days > 1 and days <=7):
            count1_7 += 1
        elif(days > 7 and days <=30):
            count7_30 += 1
        elif(days > 30):
            countgreater30 += 1

    values = [countlower1, count1_7, count7_30, countgreater30]



    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%".format(pct, absolute)

    plt.pie(values,
            labels = ['Menos de 1 dia anunciado', '1 a 7 dias anunciado', '7 a 30 dias anunciado', 'Mais de 30 dias anunciado'],
            autopct = lambda pct: func(pct, values))
    
    plt.title("Percentual de Distribuição de Dias Criação do Anúncio")
    
    plt.show() 


def most_expensive_models():
    df = get_dataframe()

    cars = []

    for index, row in df.iterrows():

        price = row['price_processed']
        model = row['model_parsed']
        brand = row['brand_parsed']

        if price == '':
            continue

        cars.append({'model': f'{brand} - {model}','price': int(price)})


    cars.sort(key=lambda _model: _model['price'], reverse=True)

    top10 = cars[:10]

    plt.figure(figsize = (10, 5))

    values = list(map(lambda x: x['price'], top10))

    models = []
    index = 0
    for model in top10:
        index += 1
        models.append(f'{index} - {model["model"]}')

    plt.bar(models, values, color ='green',
            width = 0.4)
    
    plt.xlabel("Modelo")
    plt.ylabel('Preço (R$)')

    title = "Top 10 anúncios com maiores preços"

    plt.title(title)

    plt.xticks(rotation=30, ha='right')

    for i in range(len(values)):
        plt.text(i,values[i],values[i])

    plt.show()


def pie_type():

    types = []

    df = get_dataframe()
    for index, row in df.iterrows():
        
        type = row['type']

        if type == '':
            continue

        type_found = next(
            (obj for obj in types if obj['name'] == type),
            None
        )

        if type_found is None:
            type_found = {'name': type, 'count': 0}
            types.append(type_found)
        
        type_found['count'] += 1

    values = list(map(lambda x: x['count'], types))

    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%".format(pct, absolute)

    plt.pie(values,
            labels = list(map(lambda x: x['name'], types)),
            autopct = lambda pct: func(pct, values))
    
    plt.title("Percentual de distribuição dos tipos anúncios")
    
    plt.show() 

def cambios_year(isManual):

    years = []

    df = get_dataframe()
    for index, row in df.iterrows():
        
        year = int(row['ano'])
        cambio = row['cambio']

        if cambio == '' or year < 2000:
            continue

        isManual = cambio == 'Manual'

        year_found = next(
            (obj for obj in years if obj['year'] == year),
            None
        )

        if year_found is None:
            year_found = {'year': year, 'countAut': 0, 'countMan': 0}
            years.append(year_found)
        
        if isManual:
            year_found['countMan'] += 1
        else:
            year_found['countAut'] += 1

    years.sort(key=lambda _model: _model['year'])

    x = []
    y1 = []
    y2 = []

    for year in years:
        total = year['countMan'] + year['countAut']
        x.append(year['year'])
        y1.append((year['countMan']/total)*100)
        y2.append((year['countAut']/total)*100)

    plt.figure(figsize =(10, 7))
    plt.plot(x, y1, 
            color='green',   
            linewidth=1.0,
            label="Manual"
            )
    plt.plot(x, y2, 
            color='blue',   
            linewidth=1.0,
            label="Automático"
            )

    plt.legend(loc='upper left')
    
    plt.title(f'Distribuição de Tipos de Câmbios ao Longo do Anos (%)')

    plt.show()
    

def box_plot_prices():

    values = []

    df = get_dataframe()
    for index, row in df.iterrows():
        
        price = row['price_processed']
        outlier = row['price_outlier']

        if price == '':
            continue

        values.append(int(row['price_processed']))

    s = pd.Series(values)
    print(s.describe().apply(lambda x: format(x, 'f')))

    plt.figure(figsize =(10, 7))
 
    plt.boxplot(values)
    plt.title("Box plot preços automóveis")

    
    plt.show()

def top_electric(average_price):

    models = []

    df = get_dataframe()
    for index, row in df.iterrows():

        combustivel = row['combustivel']
        model = row['model_parsed']
        brand = row['brand_parsed']
        price = row['price']
        brand_model_joined = f'{brand} - {model}'

        if combustivel == '' or price == '' or not('Híbrido' in combustivel or 'Elétrico' == combustivel) or model == 'ONIX' or model == 'ETIOS':
            continue

        model_found = next(
            (obj for obj in models if obj['name'] == brand_model_joined),
            None
        )

        if model_found is None:
            model_found = {'name': brand_model_joined, 'count': 0, 'sum': 0, 'average': 0}
            models.append(model_found)
        
        model_found['count'] += 1
        model_found['sum'] += int(price)
        model_found['average'] = round(model_found['sum'] / model_found['count'])

    models.sort(key=lambda _model: _model['count'], reverse=True)

    top10 = models[:10]

    _models = list(map(lambda x: x['name'], top10))
    _values = list(map(lambda x: x['average' if average_price else 'count'], top10))

    plt.figure(figsize = (10, 5))
    
    plt.bar(_models, _values, color ='green',
            width = 0.4)
    
    plt.xlabel("Modelo")
    plt.ylabel('Preço Médio (R$)' if average_price else 'Quantidade')

    title = "Preço médio dos top 10 modelos elétricos/híbridos com mais anúncios" if average_price else "Top 10 modelos elétricos/híbridos com mais anúncios"

    plt.title(title)

    plt.xticks(rotation=30, ha='right')

    for i in range(len(_models)):
        plt.text(i,_values[i],_values[i])

    plt.show()

def average_city(min_city):
    cities = []

    df = get_dataframe()
    for index, row in df.iterrows():

        city = row['city_processed']
        price = row['price_processed']
        outlier = row['price_outlier']

        if price == '' or outlier == 'TALVEZ' or outlier == 'AMOSTRA PEQUENA':
            continue

        city_found = next(
            (obj for obj in cities if obj['name'] == city),
            None
        )

        if city_found is None:
            city_found = {'name': city, 'count': 0, 'sum': 0}
            cities.append(city_found)
        
        city_found['count'] += 1
        city_found['sum'] += int(price)
        city_found['average_price'] = round(city_found['sum']/city_found['count'])

    cities = list(filter(lambda _city: _city['count'] >= min_city, cities))

    cities.sort(key=lambda _city: _city['average_price'], reverse=True)

    top10 = cities[:10]

    _cities = list(map(lambda x: x['name'], top10))
    _values = list(map(lambda x: x['average_price'], top10))

    plt.figure(figsize = (10, 5))
    
    plt.bar(_cities, _values, color ='green',
            width = 0.4)
    
    plt.xlabel("Cidade")
    plt.ylabel("Média de preço (R$)")
    plt.title(f'Top 10 cidades com maiores preços médios {"(mais de " + str(min_city) + " anúncios)" if min_city > 1 else ""}')
    plt.xticks(rotation=30, ha='right')

    for i in range(len(_cities)):
        plt.text(i,_values[i],_values[i])

    plt.show()


def most_city():
    cities = []

    df = get_dataframe()
    for index, row in df.iterrows():
        city = row['city_processed']

        city_found = next(
            (obj for obj in cities if obj['name'] == city),
            None
        )

        if city_found is None:
            city_found = {'name': city, 'count': 0}
            cities.append(city_found)
        
        city_found['count'] += 1

    cities.sort(key=lambda _city: _city['count'], reverse=True)

    top10 = cities[:10]

    _cities = list(map(lambda x: x['name'], top10))
    _values = list(map(lambda x: x['count'], top10))

    plt.figure(figsize = (10, 5))
    
    plt.bar(_cities, _values, color ='green',
            width = 0.4)
    
    plt.xlabel("Cidade")
    plt.ylabel("Quantidade de anúncios")
    plt.title("Top 10 cidades com mais anúncios")
    plt.xticks(rotation=30, ha='right')

    for i in range(len(_cities)):
        plt.text(i,_values[i],_values[i])

    plt.show()

def chart_most_brands():

    brands = []

    df = get_dataframe()
    for index, row in df.iterrows():
        brand = row['brand_parsed']

        brand_found = next(
            (obj for obj in brands if obj['name'] == brand),
            None
        )

        if brand_found is None:
            brand_found = {'name': brand, 'count': 0}
            brands.append(brand_found)
        
        brand_found['count'] += 1

    brands.sort(key=lambda _brands: _brands['count'], reverse=True)

    top10 = brands[:10]

    _brands = list(map(lambda x: x['name'], top10))
    _values = list(map(lambda x: x['count'], top10))

    plt.figure(figsize = (10, 5))
    
    plt.bar(_brands, _values, color ='green',
            width = 0.4)
    
    plt.xlabel("Marca")
    plt.ylabel("Quantidade de anúncios")
    plt.title("Top 10 marcas com mais anúncios")

    for i in range(len(_brands)):
        plt.text(i,_values[i],_values[i])

    plt.show()

def chart_most_models():

    brands_models = []

    df = get_dataframe()
    for index, row in df.iterrows():
        brand = row['brand_parsed']
        model = row['model_parsed']
        brand_model_joined = f'{brand} - {model}'

        brand_model_found = next(
            (obj for obj in brands_models if obj['name'] == brand_model_joined),
            None
        )

        if brand_model_found is None:
            brand_model_found = {'name': brand_model_joined, 'count': 0}
            brands_models.append(brand_model_found)
        
        brand_model_found['count'] += 1

    brands_models.sort(key=lambda _brands: _brands['count'], reverse=True)

    top10 = brands_models[:10]

    _brands = list(map(lambda x: x['name'], top10))
    _values = list(map(lambda x: x['count'], top10))

    plt.figure(figsize = (10, 5))
    
    plt.bar(_brands, _values, color ='green',
            width = 0.4)
    
    plt.xlabel("Marca - Modelo")
    plt.ylabel("Quantidade de anúncios")
    plt.title("Top 10 modelos com mais anúncios")
    plt.xticks(rotation=30, ha='right')

    for i in range(len(_brands)):
        plt.text(i,_values[i],_values[i])

    plt.show()