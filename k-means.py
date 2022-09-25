# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from Cluster_Standard_Dev import * 
# from common_functions import*
# from sklearn.cluster import KMeans
# import pickle


# df1 = pd.read_csv(r"sample_data.csv")
# vector_l=[]
# for _, row  in df1.iterrows():
#   vector_l.append(calculate_vector(row['organization_name']))

# ##k= 3107,3190,3200
# kmeans = KMeans(n_clusters=15)
# clusters= kmeans.fit(vector_l)

# filename = 'finalized_model3.sav'
# pickle.dump(clusters, open(filename, 'wb'))
 
# # some time later...
 
# # load the model from disk
# loaded_model = pickle.load(open(filename, 'rb'))


# pred = []
# for vec in vector_l:
#   pred.append(loaded_model.predict(vec[np.newaxis, :]))

# df1.insert(0,'Clusters',pred,True)
# df1.to_csv('output1.csv')



import string



s= 'f. j. davey home'
s.translate(str.maketrans('', '', string.punctuation))
word=''
for i in s:
    if len(i)==1:
        s.strip(i)
        word+=i
print(word.join(s))
