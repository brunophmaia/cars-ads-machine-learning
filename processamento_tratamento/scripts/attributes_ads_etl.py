from datetime import datetime
import pandas as pd
import unidecode

from mg_cities.cities import getCitiesProcessed, getCityFromSemiProfissional

def join_dfs(df_olx, df_seminovos):
    del df_olx["publish_date"]
    del df_olx["sell_diffs"]
    del df_olx["attrs_values"]
    del df_olx["attrs_keys"]
    del df_olx["items"]
    del df_olx["url"]
    del df_olx["read_date"]
    del df_olx["city"]

    del df_seminovos["publish_date"]
    del df_seminovos["motor"]
    del df_seminovos["brand_model"]
    del df_seminovos["attrs_keys"]
    del df_seminovos["attrs_values"]
    del df_seminovos["items"]
    del df_seminovos["address"]
    del df_seminovos["read_date"]

    frames = [df_olx, df_seminovos]

    df_joined = pd.concat(frames)

    df_joined.to_csv('step_5_items_extracted\\ads.csv', sep=';', encoding='utf-8', index=False)

def ad_new_cols(df):
    df['posted_days'] = ''
    df['exchange'] = ''
    df['leilao'] = ''
    df['portas'] = ''
    df['cambio'] = ''
    df['direcao'] = ''
    df['quilometragem'] = ''
    df['ano'] = ''
    df['combustivel'] = ''
    df['motorizacao'] = ''
    df['cor'] = ''
    df['vidros_eletricos'] = ''
    df['air_bag'] = ''
    df['sensor_estacionamento'] = ''
    df['som'] = ''
    df['blindado'] = ''
    df['alarme'] = ''
    df['camera_re'] = ''
    df['ar_condicionado'] = ''
    df['trava_eletrica'] = ''
    df['completo'] = ''
    df['city_processed'] = ''


def process_price_olx(row, index, df_olx):
    price = row['price']
    price = price.replace('.','')
    price = price if price.isdigit() else ''
    df_olx.at[index,'price'] = price

def process_price_seminovos(row, index, df_seminovos):
    price = row['price']
    price = price.split(',')[0].replace(".",'')
    price = price if price.isdigit() else ''
    df_seminovos.at[index,'price'] = price

def process_posted_days_olx(row, index, df_olx):
    publish_date = row['publish_date']
    read_date = row['read_date']
    read_date = datetime.strptime(read_date, "%d/%m/%Y")

    publish_date = publish_date.replace('Publicado em ', '')
    publish_date = f'{publish_date.split(" ")[0]}/2022'
    publish_date = datetime.strptime(publish_date, "%d/%m/%Y")
    df_olx.at[index,'posted_days'] = (read_date - publish_date).days

def process_posted_days_seminovos(row, index, df_seminovos):
    publish_date = row['publish_date']
    read_date = row['read_date']
    read_date = datetime.strptime(read_date, "%d/%m/%Y")

    publish_date = datetime.strptime(publish_date, "%d/%m/%Y")
    df_seminovos.at[index,'posted_days'] = (read_date - publish_date).days

def process_aceita_troca_olx(row, index, df_olx):
    diffs = row['sell_diffs'].split(",")
    aceita_troca = ''

    if 'Aceita troca' in diffs:
        aceita_troca = 'Sim'
    elif 'Não aceita troca' in diffs:
        aceita_troca = 'Não'
    
    df_olx.at[index,'exchange'] = aceita_troca

def attr_in_keys(df, index, row, column, key, dic_replace, default_final_value, keep_found):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = default_final_value
    indexKey = None

    try:
        indexKey = attrs_keys.index(key)
    except ValueError:
        indexKey = -1
    
    if(indexKey >= 0):
        value = attrs_values[indexKey]

        if value in dic_replace:
            final_value = dic_replace[value]
        elif keep_found:
            final_value = value

    df.at[index, column] = final_value

def value_in_items(df, index, row, new_column, column_items, values, value_if_has, value_if_has_not):
    items = row[column_items].split(",")
    final_value = value_if_has_not

    for value in values:
        if value in items:
            final_value = value_if_has

    df.at[index,new_column] = final_value

def process_direcao_seminovos(df, index, row, new_column, column_items):
    items = row[column_items].split(",")
    final_value = 'Mecânica'
    
    if('DIREÇÃO ELÉTRICA' in items):
        final_value = 'Elétrica'
    elif('DIREÇÃO HIDRÁULICA' in items):
        final_value = 'Hidráulica'

    df.at[index,new_column] = final_value

def process_km_olx(df, index, row, column, key):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexKey = None

    try:
        indexKey = attrs_keys.index(key)
    except ValueError:
        indexKey = -1
    
    if(indexKey >= 0):
        value = attrs_values[indexKey]

        if value.isdigit():
            final_value = value

    df.at[index, column] = final_value

def process_km_seminovos(df, index, row, column, key):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexKey = None

    try:
        indexKey = attrs_keys.index(key)
    except ValueError:
        indexKey = -1
    
    if(indexKey >= 0):
        value = attrs_values[indexKey]
        value = value.upper()

        if 'KM' in value:
            final_value = value.split('KM')[0].strip().replace(".","")

    df.at[index, column] = final_value

def process_ano_olx(df, index, row, column, key):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexKey = None

    try:
        indexKey = attrs_keys.index(key)
    except ValueError:
        indexKey = -1
    
    if(indexKey >= 0):
        value = attrs_values[indexKey]

        if value == '1950 ou anterior':
            final_value = '1950'
        else:
            final_value = value

    df.at[index, column] = final_value

def process_ano_seminovos(df, index, row, column, key):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexKey = None

    try:
        indexKey = attrs_keys.index(key)
    except ValueError:
        indexKey = -1
    
    if(indexKey >= 0):
        value = attrs_values[indexKey]
        final_value = value.split('/')[1]

    df.at[index, column] = final_value

def process_combustivel_olx(df, index, row, column, key_combustivel, key_gnv):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexCombustivel = None

    try:
        indexCombustivel = attrs_keys.index(key_combustivel)
    except ValueError:
        indexCombustivel = -1
    
    if(indexCombustivel >= 0):
        valueCombustivel = attrs_values[indexCombustivel]

        if valueCombustivel == 'Flex':
            valueCombustivel = 'Bi-Combustível'

        indexGnv = None
        try:
            indexGnv = attrs_keys.index(key_gnv)
        except ValueError:
            indexGnv = -1

        if(indexCombustivel >= 0):
            valueGnv = attrs_values[indexGnv]

            if(valueGnv == 'Sim'):
                valueCombustivel = f'{valueCombustivel} + Kit Gás'

        final_value = valueCombustivel

    df.at[index, column] = final_value

def process_combustivel_seminovos(df, index, row, column, key_combustivel):
    attrs_keys = row['attrs_keys'].split(',')
    attrs_values = row['attrs_values'].split(',')

    final_value = ''
    indexCombustivel = None

    try:
        indexCombustivel = attrs_keys.index(key_combustivel)
    except ValueError:
        indexCombustivel = -1
    
    if(indexCombustivel >= 0):
        valueCombustivel = attrs_values[indexCombustivel]

        if valueCombustivel == 'Kit Gás':
            valueCombustivel = 'Gás Natural'
        elif valueCombustivel == 'Hibrido (combustão + elétrico)':
            valueCombustivel = 'Híbrido'

        final_value = valueCombustivel

    df.at[index, column] = final_value


def process_motor_seminovos(df_seminovos, index, row, column):

    final_value = ''

    try:
        motor = float(row['motor'])

        if(motor > 0 and motor < 2):
            final_value = motor
        elif(motor >= 2 and motor < 3):
            final_value = '2.0'
        elif(motor >= 3 and motor < 4):
            final_value = '3.0'
        elif(motor >= 4):
            final_value = '4.0'
    except:
        final_value = ''

    df_seminovos.at[index, column] = final_value

def process_city_olx(df_olx, index, row, column, cities):

    city = df_olx['city']
    city = row['city']
    city = unidecode.unidecode(city).upper()
    city = city.split(',')[1].strip() if ',' in city else city.strip()

    city = 'AMPARO DO SERRA' if city == 'AMPARO DA SERRA' else city
    city = 'BRASOPOLIS' if city == 'BRAZOPOLIS' else city
    city = 'PASSA VINTE' if city == 'PASSA 20' else city
    city = 'SAO JOAO DEL REI' if city == 'SAO JOAO DEL REY' else city
    city = 'TRES CORACOES' if city == '3 CORACOES' else city
    city = 'SETE LAGOAS' if city == '7 LAGOAS' else city

    if city not in cities:
        city = ''
    
    df_olx.at[index, column] = city

def process_city_seminovos(df_seminovos, index, row, column, cities):
    address = row['address']
    type = row['type']

    city = unidecode.unidecode(address).upper().strip() if type == 'Particular' else getCityFromSemiProfissional(address)

    if city not in cities:
        city = ''

    df_seminovos.at[index, column] = city

def process_completo(df, index, row, column):

    hasDirecao = row['direcao'] != 'Mecânica'
    hasVidros = row['vidros_eletricos'] == 'Sim'
    hasAlarme = row['alarme'] == 'Sim'
    hasArCondicionado = row['ar_condicionado'] == 'Sim'
    hasTravas = row['trava_eletrica'] == 'Sim'

    df.at[index, column] = 'Sim' if hasDirecao and hasVidros and hasAlarme and hasArCondicionado and hasTravas else 'Não'

def process_completo_final_dataframe(df):
    for index, row in df.iterrows():
        process_completo(df, index, row, 'completo')
    
#####################################################

def olx_attrs_etl(df_olx):
    ad_new_cols(df_olx)
    cities = getCitiesProcessed()

    for index, row in df_olx.iterrows():
        process_price_olx(row, index, df_olx)
        process_posted_days_olx(row, index, df_olx)
        process_aceita_troca_olx(row, index, df_olx)
        value_in_items(df_olx, index, row, 'leilao', 'sell_diffs', ['Carro de leilão'], 'Sim', 'Não')
        attr_in_keys(df_olx, index, row, 'portas', 'Portas', {'4 portas': '4portas', '2 portas': '2portas'}, '', False)
        attr_in_keys(df_olx, index, row, 'cambio', 'Câmbio', {'Manual': 'Manual', 'Automático': 'Automático', 'Semi-Automático': 'Automatizado'}, '', False)
        attr_in_keys(df_olx, index, row, 'direcao', 'Direção', {'Hidráulica': 'Hidráulica', 'Mecânica': 'Mecânica', 'Elétrica': 'Elétrica', 'Assistida': 'Mecânica'}, '', False)
        process_km_olx(df_olx, index, row, 'quilometragem', 'Quilometragem')
        process_ano_olx(df_olx, index, row, 'ano', 'Ano')
        process_combustivel_olx(df_olx, index, row, 'combustivel', 'Combustível', 'Kit GNV')
        attr_in_keys(df_olx, index, row, 'motorizacao', 'Potência do motor', {'2.0 - 2.9': '2.0', '3.0 - 3.9': '3.0', '4.0 ou mais': '4.0'}, '', True)
        attr_in_keys(df_olx, index, row, 'cor', 'Cor', {'Outra': ''}, '', True)
        value_in_items(df_olx, index, row, 'vidros_eletricos', 'items', ['Vidro elétrico'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'air_bag', 'items', ['Air bag'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'sensor_estacionamento', 'items', ['Sensor de ré'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'som', 'items', ['Som'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'blindado', 'items', ['Blindado'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'alarme', 'items', ['Alarme'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'camera_re', 'items', ['Câmera de ré'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'ar_condicionado', 'items', ['Ar condicionado'], 'Sim', 'Não')
        value_in_items(df_olx, index, row, 'trava_eletrica', 'items', ['Trava elétrica'], 'Sim', 'Não')
        process_completo(df_olx, index, row, 'completo')
        process_city_olx(df_olx, index, row, 'city_processed', cities)
        

def seminovos_attrs_etl(df_seminovos):
    ad_new_cols(df_seminovos)
    cities = getCitiesProcessed()

    for index, row in df_seminovos.iterrows():
        process_price_seminovos(row, index, df_seminovos)
        process_posted_days_seminovos(row, index, df_seminovos)
        attr_in_keys(df_seminovos, index, row, 'exchange', 'Troca?', {'Aceito Troca': 'Sim', 'Não Aceita Troca': 'Não'}, '', False)
        attr_in_keys(df_seminovos, index, row, 'leilao', 'Leilão', {'Proveniente de leilão': 'Sim'}, 'Não', False)
        attr_in_keys(df_seminovos, index, row, 'portas', 'Portas', {'0': '2portas', '1': '2portas', '2': '2portas',  '3': '4portas', '4': '4portas', '5': '4portas', '6': '4portas'}, '', False)
        attr_in_keys(df_seminovos, index, row, 'cambio', 'Câmbio', {'Manual': 'Manual', 'Automático': 'Automático', 'Automatizado': 'Automatizado', 'Não Informado': ''}, '', False)
        process_direcao_seminovos(df_seminovos, index, row, 'direcao', 'items')
        process_km_seminovos(df_seminovos, index, row, 'quilometragem', 'Quilometragem')
        process_ano_seminovos(df_seminovos, index, row, 'ano', 'Ano - Modelo')
        process_combustivel_seminovos(df_seminovos, index, row, 'combustivel', 'Combustível')
        process_motor_seminovos(df_seminovos, index, row, 'motorizacao')
        attr_in_keys(df_seminovos, index, row, 'cor', 'cor', {}, '', True)
        value_in_items(df_seminovos, index, row, 'vidros_eletricos', 'items', ['VIDROS ELÉTRICOS'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'air_bag', 'items', ['AIR BAGS 12', 'AIR BAGS 9', 'AIR BAGS 4', 'AIR BAGS 11', 'AIR BAGS 7', 'AIR BAGS 6', 'AIR BAGS 1', 'AIR BAGS 2', 'AIR BAGS 10', 'AIR BAGS 8', 'AIR BAGS 3', 'AIR BAGS 5'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'sensor_estacionamento', 'items', ['SENSOR DE ESTACIONAMENTO'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'som', 'items', ['DVD', 'MP3 / USB', 'CD / MP3', 'CENTRAL MULTIMIDIA'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'blindado', 'items', ['BLINDADO'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'alarme', 'items', ['ALARME'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'camera_re', 'items', ['CÂMERA DE RÉ'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'ar_condicionado', 'items', ['AR CONDICIONADO', 'AR-COND. DIGITAL'], 'Sim', 'Não')
        value_in_items(df_seminovos, index, row, 'trava_eletrica', 'items', ['TRAVAS ELÉTRICAS'], 'Sim', 'Não')
        process_completo(df_seminovos, index, row, 'completo')
        process_city_seminovos(df_seminovos, index, row, 'city_processed', cities)

#####################################################


def print_attributes_olx(df_olx):

    set_diffs = set()
    set_keys_olx = set()
    set_items_olx = set()

    for index, row in df_olx.iterrows():
        sell_diffs = row['sell_diffs'].split(',')
        keys = row['attrs_keys'].split(',')
        items = row['items'].split(',')

        for set_diff in sell_diffs:
            set_diffs.add(set_diff)
        for key in keys:
            set_keys_olx.add(key)
        for item in items:
            set_items_olx.add(item)

    print('\nDiferenciais de venda Olx:\n')
    print(set_diffs)
    print('\nChaves atributos Olx:\n')
    print(set_keys_olx)
    print('\nItems Olx:\n')
    print(set_items_olx)

def print_attributes_seminovos(df_seminovos):

    set_keys_seminovos = set()
    set_items_seminovos = set()

    for index, row in df_seminovos.iterrows():
        keys = row['attrs_keys'].split(',')
        items = row['items'].split(',')

        for key in keys:
            set_keys_seminovos.add(key)
        for item in items:
            set_items_seminovos.add(item)

    print('\n\nChaves atributos Seminovos:\n')
    print(set_keys_seminovos)
    print('\nItems Seminovos:\n')
    print(set_items_seminovos)
    print('\n')


def printValuesFromKey(df, key):

    setValues = set()

    for index, row in df.iterrows():
        keys = row['attrs_keys'].split(',')
        values = row['attrs_values'].split(',')
        
        indexKey = None

        try:
            indexKey = keys.index(key)
        except ValueError:
            indexKey = -1

        if indexKey >= 0:
            setValues.add(values[indexKey])
    
    print(setValues)