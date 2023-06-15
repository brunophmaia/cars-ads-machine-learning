import pandas as pd

def get_dataframe():
    df = pd.read_csv('ads.csv', sep=';')
    df = df.fillna('')
    return df