import pandas as pd
import numpy as np

# 유클리드 거리 공식
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

# input - weather
# output - drink list
# temp, cloud, faliing : int
def recommend(temp, cloud, falling):
    by_weather = pd.read_csv('data/feature_by_weather_without_iceamericano.csv', encoding = 'cp949')
    weather_group = by_weather[(by_weather['기온'] == temp) & (by_weather['흐림'] == cloud) & (by_weather['비소나기눈'] == falling)]
    weight_feature = weather_group.drop(['기온', '흐림', '비소나기눈'], axis=1).to_numpy()
    
    by_avg_weather = pd.read_csv('data/ratio_features_without_iceamericano.csv', encoding = 'cp949')
    avg_weather_group = by_avg_weather[(by_avg_weather['기온'] == temp) & (by_avg_weather['흐림'] == cloud) & (by_avg_weather['비소나기눈'] == falling)]
    avg_weight_feature = avg_weather_group.drop(['기온', '흐림', '비소나기눈'], axis=1).to_numpy()
    
    drink_feature = pd.read_csv('data/features_without_iceamericano.csv', encoding = 'cp949').drop(['Unnamed: 0'], axis=1)
    
    result = [] # 유사도 계산 결과
    result_avg = [] # 유사도 계산 결과
    
    for i in range(len(drink_feature)):
        drink = drink_feature.iloc[i, 1:].to_numpy().astype('float')
        
        distance = euclidean_distance(weight_feature, drink)
        distance_avg = euclidean_distance(avg_weight_feature, drink)
        
        result.append(distance)
        result_avg.append(distance_avg)
    
    min_idx = []
    min_idx_avg = []
    sorted_indices = sorted(range(len(result)), key=lambda i: result[i])
    sorted_indices_avg = sorted(range(len(result_avg)), key=lambda i: result_avg[i])
    
    for i in range(3):
        min_idx.append(sorted_indices[i])
    
    for i in range(6):
        min_idx_avg.append(sorted_indices_avg[i])

    min_items = []
        
    for i in range(len(min_idx)):
        min_items.append(drink_feature.loc[min_idx[i], 'items'])
  
    min_items_avg = []
    
    for j in range(len(min_idx_avg)):
        min_items_avg.append(drink_feature.loc[min_idx_avg[j], 'items'])
        
    count = 0
    for i in range(len(min_items_avg)):
        if min_items_avg[i] not in min_items:
            min_items.append(min_items_avg[i])
            count = count +1
        else:
            continue;

        if count == 3:
            break;

    return min_items