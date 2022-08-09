import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Hotel


# CSV file into a dataframe df
def combined_feature(row):
    return row['name'] + " " + row['location'] + "" + row['cuisine']


def get_id_from_index(df, index):
    return df[df.index == index]["id"].values[0]


def get_index_from_id(df, id):
    return df[df.id == id].index.values[0]


def get_recommendation_for_hotel(hotel_id):
    df = pd.DataFrame(list(Hotel.objects.all().values()))
    features = ['name','location', 'cuisine']
    for feature in features:
        df[feature] = df[feature].fillna('')

    df["combined_features"] = df.apply(combined_feature, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)

    id = get_index_from_id(df, hotel_id)

    similar_hotels = list(enumerate(cosine_sim[id]))

    sorted_similar_hotels = sorted(
        similar_hotels, key=lambda x: x[1], reverse=True)

    i = 0
    hotel_ids = []
    for hotel in sorted_similar_hotels:
        i = i + 1
        hotel_ids.append(get_id_from_index(df, hotel[0]))

        if i > 10:
            break

    return hotel_ids
