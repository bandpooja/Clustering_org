import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# from common_functions import clean_org_name


df = pd.read_csv(r"train_data.csv")
words_for_count = set()
words = set()

for _, row in df.iterrows():
    # print(row)
    org_name = row['organization_name'].lower().split(' ') 
    for w in org_name:
        if w in words_for_count:
            words.add(w)
        else:
            words_for_count.add(w)

print(f"Number of words in the dictionary are {len(words)}")

word_map = {}
for idx, w in enumerate(words):
    word_map[w] = idx

df = pd.read_csv(r"sample_data.csv")
vecs = []
ws = [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.1]
for _, row in df.iterrows():
    vec = np.zeros(len(word_map))

    org_name = row['organization_name'].lower().split(' ')
    # org_name = clean_org_name(org_name_).lower()
    print(org_name)
    for idx, w in enumerate(org_name):
        if idx < len(ws):
            if w in word_map:
                vec[word_map[w]] = ws[idx]
    vecs.append(vec)

kmeans = KMeans(n_clusters=29)
clusters= kmeans.fit(vecs)

pred = []
for vec in vecs:
  pred.append(clusters.predict(vec[np.newaxis, :]))

df['Predicted Cluster'] = pred
df.to_csv('output1.csv')
