from turtle import color
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from Cluster_Standard_Dev import * 
from common_functions import*
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage


# #cluster_cen = calculate_average()
# cluster_std = calculate_std()
# cluster_plot, cluster_cen= calculate_average_plot()
# vec_list=[]
# for i in cluster_cen.keys():
#   vec_list.append(cluster_cen[i])

# count_list=[]
# for i in cluster_plot.keys():
#   count_list.append(cluster_plot[i])


#Sc = StandardScaler()
# X = Sc.fit_transform(vec_list)
# pca = PCA(2) 
# pca_data = pd.DataFrame(pca.fit_transform(X),columns=['PC1','PC2'])


# i=0
# x = []
# y = []
# s = []
# for idx, j in enumerate(cluster_std.keys()):
#   x.append(pca_data['PC1'][idx])
#   y.append(pca_data['PC2'][idx])
#   s.append(2*cluster_std[j])

# plt.scatter(x, y, s)
# plt.savefig('clusters.png')


# pca_1=PCA(1)
# X1 = Sc.fit_transform(vec_list)
# pca_data_1 = pd.DataFrame(pca_1.fit_transform(X1),columns=['PC1'])
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# clusters = pca_data_1['PC1']
# count_org = count_list
# #my_colors = 'rgbkymc'
# ax.bar(clusters,count_org,color='r')
# plt.savefig('clusters_bar.png')


# df1 = pd.read_csv(r"train_data.csv")
# vector_l=[]
# for _, row  in df1.iterrows():
#   vector_l.append(calculate_vector(row['organization_name']))



# X2 = Sc.fit_transform(vector_l)
# pca2 = PCA(2) 
# pca_data2 = pd.DataFrame(pca2.fit_transform(X2),columns=['PC1','PC2'])
# # plt.scatter(pca_data2['PC1'],pca_data2['PC2'])
# # plt.savefig('clusters1.png')





# data = list(zip(pca_data2['PC1'],pca_data2['PC2'] ))
# inertias = []
# K= range(3179,3200,5)
# for i in list(K):
#     print(i)
#     kmeans = KMeans(n_clusters=i)
#     kmeans.fit(data)
#     inertias.append(kmeans.inertia_)

# plt.plot(K, inertias, marker='o')
# plt.title('Elbow method')
# plt.xlabel('Number of clusters')
# plt.ylabel('Inertia')
# plt.savefig('kmeans1.png')


# linkage_data = linkage(data, method='ward', metric='euclidean')
# dendrogram(linkage_data)
# ##plt.show()
# plt.savefig('dendo.png')


x = np.linspace(0,100)

def fun_val(x):
  if x < 10:
    return 1
  
  y = np.log(100 - x)/np.log(100-10)
  return y


y = [fun_val(v) for v in x]

plt.plot(x,y)
plt.ylim(0, 1)

plt.show()






