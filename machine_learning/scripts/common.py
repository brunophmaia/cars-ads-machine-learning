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