import matplotlib.pyplot as plt
import os
import os.path as osp
import pandas as pd
from wordcloud import WordCloud

from preprocess_constants import conversions
from preprocess import clean_org_name, perform_conversions, remove_abbreviation, remove_weird_characters, remove_stop_words


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
        looking at the wordcloud it can be seen that there are a lot of words with similar meaning in different forms
         which occur more regularly in the cloud.

        Combining them in a file and then removing them in preprocessing step
        defining this list in the preprocess.py file
    '''
    organizations = remove_abbreviation(org_name=organizations)
    organizations = perform_conversions(s=organizations)
    
    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(organizations)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(osp.join(result_loc, 'wordCloudPostCleaning.png'))
    #endregion

    #region cleaning and generating a new df
    corrected_organization_names = []
    for org in organization_names:
        org = org.lower() + " "
        corrected_organization_names.append(clean_org_name(org=org))

    df['clean_organization_name'] = corrected_organization_names
    df.to_csv(osp.join(result_loc, 'clean_train_df.csv'))
    #endregion



if __name__ == "__main__":
    train_csv = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results\\data\\input\\train_data.csv"
    result_loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results"
    word_cloud_cleaning(train_csv, result_loc)
