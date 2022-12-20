import concurrent.futures
import numpy as np
import os as osp
import pandas as pd
import threading

# matrix= np.array_split(final_df,5)

# #matrix = [[1, 2],[3, 4],[5, 6]]

# def min(n, **total):
#     matrix[n].index= pd.RangeIndex(0,len(matrix[n]))
#     for i in range(len(matrix[n])):
#         distance= np.linalg.norm(point - matrix[n]['center'][i])
#         if distance < matrix[n]['radius'][i]:
#             pred_list.append(df.loc[df.number == matrix[n]['group'][i], 'organization_name'].values[0])
#         elif minThreads["minThreads"] > distance - matrix[n]['radius'][i]:
#             minThreads['minThreads'] = distance - matrix[n]['radius'][i]
#             suggestions[df.loc[df.number == matrix[n]['group'][i], 'organization_name'].values[0]]= minThreads["minThreads"]

# minThreads ={"minThreads":max(0, np.linalg.norm(point - matrix[0]['center'][0]) -matrix[0]['radius'][0])}

# for i in range(len(matrix)):
#     t = threading.Thread(target=min, args=(i,), kwargs=minThreads)
#     print('thread ',i)
#     t.start()
# print(minThreads['minThreads'])
        

# final_df -> id,cneter,radius; df -> org_name, id; point -> to predict

def get_pred_name(org_name_n_centers: tuple):
    org_name = org_name_n_centers[0]
    centers = org_name_n_centers[1]
    # df = org_name_n_centers[2]
    pred_list_insire_r = []
    pred_list_out_r = {}
    point = org_name # vectorize
    min_dist = max(0, np.linalg.norm(point - centers['center'][0]) - centers['radius'][0])
    for _, row  in centers.iterrows():
        distance= np.linalg.norm(point - row['center'])
        if distance < (row['radius']):
             pred_list_insire_r.append(row['group'])
        elif min_dist > distance - row['radius']:
            min_dist = distance - row['radius']
            pred_list_out_r[row['group']] = min_dist
    return [pred_list_insire_r, pred_list_out_r]

# print(point)
# print(df_splits[0])

if __name__ == "__main__":    
    final_df = pd.read_pickle('C://Users//BandalPo//OneDrive - Government of Ontario//Documents//Clustering_org//data_result.pkl')
    df = pd.read_csv(osp.path.join(r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results", 'final.csv'))
    point = final_df['center'][70]
    pred_list_insire_r = []
    pred_list_out_r = {}

    results = []
    df_splits = [final_df[:int(len(final_df)/5)].reset_index(), 
        final_df[int(len(final_df)/5):2*int(len(final_df)/5)].reset_index(),
        final_df[int(2*len(final_df)/5):3*int(len(final_df)/5)].reset_index(),
        final_df[3*int(len(final_df)/5):4*int(len(final_df)/5)].reset_index(),
        final_df[4*int(len(final_df)/5):].reset_index()]
    point = final_df['center'][70]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(get_pred_name, [(point, df_split) for df_split in df_splits]):
            results.append(result)

    pred_in_r = [r_i for r in results for r_i in r[0]]
    if len(pred_in_r) > 0:
        # change row-group to organization_name
        pred_names = []
        for p in pred_in_r:
            print(p)
            df_f = df[df['number'] == p]
            print(df_f)
            pred_names = df_f['organization_name'].values.tolist()[0]
        print(f"prediction inside radius: {pred_names}")
    if len(pred_in_r) == 0:
        pred_out_r = {k:v for r in results for k,v in r[1].items()}
        sorted_suggestion_list= [k for k, v in sorted(pred_out_r.items(), key=lambda item: item[1])]
        print(f"prediction outside radius: {sorted_suggestion_list[:3]}")
