import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from scripts.common import get_dataframe, remove_missing_values

def pca_dispersion():

    relevant_cols = ['price_processed','ano','quilometragem_processed', 'posted_days', 'motorizacao']

    df_all_cols = get_dataframe()
    df_all_cols = remove_missing_values(df_all_cols, relevant_cols)

    df = df_all_cols[relevant_cols]

    scaler = StandardScaler()
    normal_data = scaler.fit_transform(df)

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(normal_data)


    print("Variância componentes principais:")
    print(pca.explained_variance_ratio_)

    plt.scatter(principal_components[:, 0], principal_components[:, 1])
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.title('Dispersão dos Componentes Principais')
    plt.show()

def pca_prediction():

    relevant_cols = ['price_processed','ano','quilometragem_processed', 'posted_days', 'motorizacao']

    df_all_cols = get_dataframe()
    df_all_cols = remove_missing_values(df_all_cols, relevant_cols + ['leilao'])
    df_all_cols = process_leilao(df_all_cols)

    df = df_all_cols[relevant_cols]

    X = df.values
    y = np.array(df_all_cols['leilao']) 

    scaler = StandardScaler()
    normal_X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(normal_X, y, test_size=0.2, random_state=42)

    y_train=y_train.astype('int')
    y_test=y_test.astype('int')

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_train)

    modelo_svm = SVC()
    modelo_svm.fit(principal_components, y_train)

    test_pc = pca.transform(X_test)

    y_pred = modelo_svm.predict(test_pc)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recallscore = recall_score(y_test, y_pred)
    f1score = f1_score(y_test, y_pred)

    print("\n")
    print("Acurácia do modelo: {:.2f}%".format(accuracy * 100))
    print("Precisão do modelo: {:.2f}%".format(precision * 100))
    print("Recall score do modelo: {:.2f}%".format(recallscore * 100))
    print("F1-score do modelo: {:.2f}%".format(f1score * 100))
    print("\n")
    

def process_leilao(df):

    for index, row in df.iterrows():

        if row['leilao'] == 'Sim':
            df.at[index,'leilao'] = 1
        else:
            df.at[index,'leilao'] = 0

    return df