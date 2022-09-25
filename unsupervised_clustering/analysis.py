import imp
import matplotlib.pyplot as plt
import os
import os.path as osp
import pandas as pd
from wordcloud import WordCloud

from preprocess import conversions, stopwords


def word_cloud_cleaning(df_path: str, result_loc: str):
    #region read data
    df = pd.read_csv(df_path)
    organization_names = df['organization_name'].values.tolist()

    organizations = " ".join(organization_names).lower()
    #endregion

    #region generating wordcloud
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(organizations)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(osp.join(result_loc, 'wordCloud.png'))
    #endregion

    #region cleaning
    '''
        looking at the wordcloud it can be seen that there are a lot of stopwords
         which occur more regularly in the cloud.

        Combining them in a file and then removing them in preprocessing step
        defining this list in the preprocess.py file
    '''
    for w in conversions.keys():
        organizations = organizations.replace(w, conversions[w])

    for w in stopwords:
        organizations = organizations.replace(w, '')
    
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(organizations)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(osp.join(result_loc, 'wordCloudPostCleaning.png'))
    #endregion

    #region cleaning and generating a new df
    corrected_organization_names = []
    for org in organization_names:
        org = org.lower() + " "
        for w in conversions.keys():
            org = org.replace(w, conversions[w])

        for w in stopwords:
            org = org.replace(w, '')
        corrected_organization_names.append(org)

    df['clean_organization_name'] = corrected_organization_names
    df.to_csv(osp.join(result_loc, 'clean_train_df.csv'))
    #endregion



if __name__ == "__main__":
    train_csv = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\Documents\\Identify_Organization\\train_data.csv"
    result_loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\Documents\\cluster_results"
    word_cloud_cleaning(train_csv, result_loc)