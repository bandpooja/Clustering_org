import json
import numpy as np
import os
import os.path as osp
import pandas as pd

def numbering(file_loc):

    df = pd.read_csv(file_loc)
    cluster= df['Predicted Cluster'].values.tolist()
    clus_dict= {}
    num=[]
    n= 60158
    for i in cluster:
        if i in clus_dict.keys():
            print('yes')
            num.append(clus_dict[i])
        else:
            print('no')
            n+=1
            clus_dict[i]= n
            num.append(n)



    # unique_cluster= list(set(cluster))
    # cluser_dict={}
    # num=1
    # for i in unique_cluster:
    #     cluser_dict[i]= num
    #     num+=1
   
    # num_list=[0] * len(cluster)

    # for i in cluser_dict.keys():
    #     for idx, j in enumerate(cluster):
    #         if i==j:
    #             print(i,j,idx,cluser_dict[i])
    #             num_list[idx]= cluser_dict[i]

    df['number'] = num
    df.to_csv(file_loc, index=0)






if __name__ == "__main__":
    loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results\\pred_20.csv"
    numbering(file_loc=loc)