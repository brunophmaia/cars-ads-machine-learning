import pandas as pd

def get_dataframe(path = None):
    df = pd.read_csv(path if path is not None else 'ads.csv', sep=';')
    df = df.fillna('')
    return df


def remove_missing_values(df, relevant_cols):

    null_indexes = []

    for index, row in df.iterrows():

        for colNull in relevant_cols:
            if row[colNull] == '':
                null_indexes.append(index)
                break
    
    df = df.drop(df.index[null_indexes])

    return df

def keep_relevant_columns(df, relevant_cols):
    _df = df[relevant_cols]
    return _df

def generate_extras_score(df):

    df['extras_score'] = ''
    binary_good_cols = ['vidros_eletricos', 'air_bag', 'sensor_estacionamento', 'som', 'blindado', 'alarme', 'camera_re', 'ar_condicionado', 'trava_eletrica']

    for index, row in df.iterrows():

        score = 0

        if row['leilao'] == 'Sim':
            score -= 5
        if row['portas'] == '4portas':
            score += 1
        if row['direcao'] == 'Hidráulica':
            score += 1
        elif row['direcao'] == 'Elétrica':
            score += 2
        
        for col in binary_good_cols:
            if(row[col] == 'Sim'):
                score += 1

        df.at[index,'extras_score'] = score

    return df