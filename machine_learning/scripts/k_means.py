from scripts.common import keep_relevant_columns, remove_missing_values, get_dataframe
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def k_means():

    relevant_cols = ['price_processed','quilometragem_processed','ano', 'posted_days', 'extras_score']

    df_all_cols = get_dataframe()
    df_all_cols = generate_extras_score(df_all_cols)
    df_all_cols = remove_missing_values(df_all_cols, relevant_cols)
    df = keep_relevant_columns(df_all_cols, relevant_cols)

    scaler = StandardScaler()
    scaler.fit(df)
    scaled_data = scaler.transform(df)

    clusters_centers, k_values = find_best_clusters(scaled_data, 12)
    generate_elbow_plot(clusters_centers, k_values)

    CLUSTERS = 6

    kmeans_model = KMeans(n_clusters = CLUSTERS)

    kmeans_model.fit(scaled_data)
    distances = kmeans_model.transform(scaled_data)

    df_all_cols["cluster"] = kmeans_model.labels_

    for i in range(CLUSTERS):
        df_all_cols[f'Distancia_cluster_{i}'] = distances[:, i]

    df_all_cols.to_csv('output\\kmeans\\k_means.csv', sep=';', encoding='utf-8', index=False)


def find_best_clusters(df, maximum_K):
    
    clusters_centers = []
    k_values = []
    
    for k in range(1, maximum_K):
        
        kmeans_model = KMeans(n_clusters = k)
        kmeans_model.fit(df)
        
        clusters_centers.append(kmeans_model.inertia_)
        k_values.append(k)
    
    return clusters_centers, k_values

def generate_elbow_plot(clusters_centers, k_values):
    
    plt.subplots(figsize = (12, 6))
    plt.plot(k_values, clusters_centers, 'o-', color = 'orange')
    plt.xlabel("Número de Clusters (K)")
    plt.ylabel("Inércia Cluster")
    plt.title("Elbow K-means")
    plt.show()

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

def k_means_count_clusters():
    df = get_dataframe('output\\kmeans\\k_means.csv')

    clusters = []

    for index, row in df.iterrows():
        cluster = row['cluster']

        cluster_found = next(
            (obj for obj in clusters if obj['cluster'] == cluster),
            None
        )

        if cluster_found is None:
            cluster_found = {'cluster': cluster, 'count': 0}
            clusters.append(cluster_found)

        cluster_found['count'] += 1

    print(clusters)

def k_means_top_near_and_far():
    df = get_dataframe('output\\kmeans\\k_means.csv')

    clusters = []

    for index, row in df.iterrows():
        cluster = row['cluster']

        cluster_found = next(
            (obj for obj in clusters if obj['cluster'] == cluster),
            None
        )

        if cluster_found is None:
            cluster_found = {'cluster': cluster, 'ads': []}
            clusters.append(cluster_found)

        cluster_found['ads'].append(row)

    for cluster in clusters:

        print(f'Cluster: {cluster["cluster"]}')

        (cluster['ads']).sort(key=lambda ad: float(ad[f'Distancia_cluster_{cluster["cluster"]}']))

        print('Próximos')
        print('Code;Marca;Modelo;Preco;Quilometragem;Ano;Dias Anuncio;Extras')

        near3 = (cluster['ads'])[:3]
        for near in near3:
            print(f'{near["code"]};{near["brand_parsed"]};{near["model_parsed"]};{near["price_processed"]};{near["quilometragem_processed"]};{near["ano"]};{near["posted_days"]};{near["extras_score"]}')

        far3 = (cluster['ads'])[-3:]
        print('Distantes')
        print('Code;Marca;Modelo;Preco;Quilometragem;Ano;Dias Anuncio;Extras')
        for far in far3:
            print(f'{far["code"]};{far["brand_parsed"]};{far["model_parsed"]};{far["price_processed"]};{far["quilometragem_processed"]};{far["ano"]};{far["posted_days"]};{far["extras_score"]}')
