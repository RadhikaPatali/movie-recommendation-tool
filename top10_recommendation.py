import pandas as pd
import numpy as np
import re
import nltk
pd.set_option('display.max_columns', None)
df = pd.read_csv("Imdb_insights.csv")
df['filtered_data'] = df['Summary'].str.lower()
df['filtered_data'] = df['filtered_data'].apply(lambda x: re.sub('[^a-zA-Z]', ' ', x))
df['filtered_data'] = df['filtered_data'].apply(lambda x: re.sub('\s+', ' ', x))
df['filtered_data'] = df['filtered_data'].apply(lambda x: nltk.word_tokenize(x))
stop_words = nltk.corpus.stopwords.words('english')
brief = []
for i in df['filtered_data']:
    data = []
    for j in i:
        if j not in stop_words and len(j) >= 3:
            data.append(j)
    brief.append(data)
brief
df['filtered_data'] = brief
df['Genre'] = df['Genre'].replace(',','')
df['Director'] = df['Director'].replace(',','')
def filter(string):
    data2 = []
    for j in string:
        data2.append(j.lower().replace(' ', ''))
    return data2
df['Genre'] = [filter(x) for x in df['Genre']]
df['Director'] = [filter(x) for x in df['Director']]
columns = ['filtered_data', 'Genre', 'Director']
data3 = []
for i in range(len(df)):
    words = ''
    for j in columns:
        words += ' '.join(df[j][i]) + ' '
    data3.append(words)
data3
df['clean_summary'] = data3
df = df[['Title', 'clean_summary']]

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tfidf = TfidfVectorizer()
features = tfidf.fit_transform(df['clean_summary'])

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(features, features)

index = pd.Series(df['Title'])

def suggest_movies_related_to(title):
    recommended = []
    idx = index[index == title].index[0]
    score = pd.Series(similarity[idx]).sort_values(ascending=False)
    list_10 = list(score.iloc[1:11].index)
    
    for i in list_10:
        recommended.append(df['Title'][i])
    return recommended
suggest_movies_related_to('The Untouchables')
