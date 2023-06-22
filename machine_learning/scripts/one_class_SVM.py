from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from scripts.common import remove_missing_values, get_dataframe
import matplotlib.pyplot as plt


def one_class_svm():

    relevant_cols = ['price_processed','ano','quilometragem_processed']

    df_all_cols = get_dataframe()
    df_all_cols = remove_missing_values(df_all_cols, relevant_cols)

    X = df_all_cols[['price_processed', 'ano','quilometragem_processed']]

    scaler = StandardScaler()
    dados = scaler.fit_transform(X)

    dados_treino, dados_teste = train_test_split(dados, test_size=0.2, random_state=42)

    modelo = OneClassSVM(kernel='rbf', gamma='scale', nu=0.1)
    modelo.fit(dados_treino)

    anomalias_teste = modelo.predict(dados_teste)

    anomalias_teste[anomalias_teste == 1] = 0  # Convertendo instâncias normais para 0
    anomalias_teste[anomalias_teste == -1] = 1  # Convertendo anomalias para 1

    y_test = [0] * len(dados_teste)
    y_test.extend([1] * len(dados_teste[anomalias_teste == -1]))

    report = classification_report(y_test, anomalias_teste)
    print(report)

def one_class_svm_chart():
    relevant_cols = ['price_processed','ano','quilometragem_processed']

    df_all_cols = get_dataframe()
    #df_all_cols = remove_not_model(df_all_cols, 'VWVOLKSWAGEN', 'GOL')
    df_all_cols = remove_missing_values(df_all_cols, relevant_cols)
    print(len(df_all_cols))

    X = df_all_cols[['price_processed', 'ano', 'quilometragem_processed']]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    #ocsvm = OneClassSVM(nu=0.005, kernel = 'rbf', gamma = 'auto') #VW-GOL
    ocsvm = OneClassSVM(nu=0.001, kernel = 'rbf', gamma = 'auto') #todos
    ocsvm.fit(X_scaled)

    anomaly_pred = ocsvm.predict(X_scaled)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X.iloc[:, 0], X.iloc[:, 1], X.iloc[:, 2], c='blue', label='Normal')

    ax.scatter(X.iloc[anomaly_pred == -1, 0], X.iloc[anomaly_pred == -1, 1], X.iloc[anomaly_pred == -1, 2], c='red', label='Anomalia')

    ax.set_xlabel('Preço')
    ax.set_ylabel('Ano')
    ax.set_zlabel('Quilometragem')
    ax.set_title('Detecção de Anomalias em Anúncios')

    ax.legend()

    plt.show()

def remove_not_model(df, brand, model):
    to_remove = []

    for index, row in df.iterrows():
        
        if(row['brand_parsed'] != brand or row['model_parsed'] != model):
            to_remove.append(index)
    
    df = df.drop(df.index[to_remove])

    return df