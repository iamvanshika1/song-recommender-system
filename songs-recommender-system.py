import pandas as pd

songs = pd.read_csv('songs.csv')

# print(songs.isnull().sum())
songs.dropna(inplace=True)

# print(songs.duplicated().sum())

songs.drop_duplicates(inplace=True)

# print(songs.duplicated().sum())

# print(songs.head())

songs['Singer/Artists'] = songs['Singer/Artists'].apply(lambda x: x.replace(" ",""))
songs['Singer/Artists'] = songs['Singer/Artists'].apply(lambda x: x.replace(",",""))
songs['Album/Movie'] = songs['Album/Movie'].apply(lambda x: x.replace(" ",""))
# print(songs.head())

songs['User-Rating'] = songs['User-Rating'].str.extract(r'(\d+\.\d+)').astype(float)

# print(songs.head())
# print(songs['User-Rating'].min())
# print(songs['User-Rating'].max())


def categorize_rating(i):
    if i<7:
        return "Poor"
    elif i>=7 and i<9:
        return "Average"
    else:
        return "Good"

songs['User-Rating'] = songs['User-Rating'].apply(categorize_rating)

# print(songs.head())

songs['tags'] = songs['Album/Movie'] + ' ' + songs['Singer/Artists'] + ' ' + songs['Genre'] + ' ' +  songs['User-Rating']

new_df = songs[['Song-Name','tags']]
# print(new_df.head())


# print(songs.shape)

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
vectors = cv.fit_transform(new_df['tags']).toarray()
# print(cv.get_feature_names_out())

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

def recommend(song):
    song_index = new_df[new_df['Song-Name']==song].index[0]
    # print(movie_index)
    distances = similarity[song_index]
    songs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:11]
    print(songs_list)

    for i in songs_list:
        print(new_df.iloc[i[0]]['Song-Name'])

recommend('Maine Tujhko Dekha')

import pickle

pickle.dump(new_df.to_dict(),open('songs.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))



