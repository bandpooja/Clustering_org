# importing Flask and other modules
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import os as osp
import multiprocessing as mp





# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        org_name = request.form.get("org")
        pred_list=make_predictions(org_name)
        return render_template("login.html",s= 'Suggestions to add in group: ',pred_list= pred_list)
    return render_template("login.html")	   


def make_predictions(org_name):
    final_df= pd.DataFrame()
    ids=[]
    avg=[]
    radius=[]
    suggestions={}
    pred_list=[]
    # for i in std_dict.keys():
    #     ids.append(i)
    #     avg.append(avg_dict[i])
    #     radius.append(std_dict[i])

    # final_df['group']=ids
    # final_df['center']=avg
    # final_df['radius']=radius

    # final_df.to_pickle('data_result.pkl')

    final_df = pd.read_pickle('C://Users//BandalPo//OneDrive - Government of Ontario//Documents//Clustering_org//data_result.pkl')
    df= pd.read_csv(osp.path.join(r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results", 'final.csv'))
    point= final_df['center'][70]

   

    min_dist= max(0, np.linalg.norm(point - final_df['center'][0]) -final_df['radius'][0])

    for _, row  in final_df.iterrows():

        distance= np.linalg.norm(point - row['center'])
        if distance < (row['radius']):
             pred_list.append(df.loc[df.number == row['group'], 'organization_name'].values[0])
        elif min_dist > distance - row['radius']:
            min_dist = distance - row['radius']
            suggestions[df.loc[df.number == row['group'], 'organization_name'].values[0]]= min_dist

    sorted_suggestion_list= {k: v for k, v in sorted(suggestions.items(), key=lambda item: item[1])}
    

    if len(pred_list)==0:
        result= list(sorted_suggestion_list.keys())[:3]
    elif len(pred_list)==1:
        result= pred_list+list(sorted_suggestion_list.keys())[:2]
    elif len(pred_list)==2:
        result= pred_list+list(sorted_suggestion_list.keys())[:1]
    else:
        result=pred_list

    return result 
	

if __name__=='__main__':
    #mp.app.run()
    
    make_predictions('1017828 Ontario Inc (J R L Contracting)')