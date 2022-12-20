from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

from unsupervised_clustering.preprocess_constants import conversions, stop_words_ctx, ignore_words


def perform_conversions(org_name: str):
    s_words = []
    ws = org_name.split(" ")
    for w in ws:
        if w.lower() in conversions.keys():
            s_words.append(conversions[w.lower()])
        else:
            s_words.append(w.lower())
    s = " ".join(s_words)
    return s


def remove_abbreviation(org_name: str):
    org_name = org_name.lower()

    org_words = org_name.split(' ')
    org_words_w_aggregated_abb = []
    for w in org_words:
        if len(w) == 1 or w == 'and':
            if len(org_words_w_aggregated_abb) == 0:
                org_words_w_aggregated_abb.append(w)
            else:
                w_l = org_words_w_aggregated_abb.pop()
                w_l += w
                org_words_w_aggregated_abb.append(w_l)
        elif len(w) == 2:
            if w[-1] == '.':
                if len(org_words_w_aggregated_abb) == 0:
                    org_words_w_aggregated_abb.append(w[0])
                else:
                    w_l = org_words_w_aggregated_abb.pop()
                    w_l += w[0]
                    org_words_w_aggregated_abb.append(w_l)
            else:
                org_words_w_aggregated_abb.append(w)
        else:
            org_words_w_aggregated_abb.append(w)
    
    org_name = " ".join(org_words_w_aggregated_abb)
    # pattern = r'(?:\.[a-z]\.)+'
    # result = re.findall(pattern, org_name)
    # if result:
    #     for r in result:
    #         pattern_w = r'(?:[a-z&])'
    #         x = re.findall(pattern_w, r)
    #         if r[-1] == ' ':
    #             org_name = org_name.replace(r, x[0]+ ' ')
    #         else:
    #             org_name = org_name.replace(r, x[0])
    
    # pattern = r'(?:\s[&])+'
    # result = re.findall(pattern, org_name)
    # if result:
    #     for r in result:
    #         org_name = org_name.replace(r, '&')
    return org_name


def remove_weird_characters(org_name: str):
    org_name = re.sub(r"[^a-zA-Z0-9\s-]", "", org_name)
    return org_name


def remove_stop_words(org_name: str):
    #stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    #ps = PorterStemmer()
    org_name_split = org_name.split(" ")
    filtered_sentence = []
    for w in org_name_split:    
        if w not in stop_words_ctx:
            if w not in ignore_words:
                filtered_sentence.append(lemmatizer.lemmatize(w.replace('-', ' ').replace("'", ""), pos='n'))
            else:
                filtered_sentence.append(w.replace('-', ' ').replace("'", ""))
            

    return (' '.join(str(x) for x in filtered_sentence if len(str(x)) > 0)) 


def clean_org_name(org_name: str):
    org_name = perform_conversions(org_name=org_name)
    #print(org_name)
    org_name = remove_abbreviation(org_name=org_name)
    #print(org_name)
    org_name = remove_weird_characters(org_name=org_name)
    #print(org_name)
    org_name = remove_stop_words(org_name=org_name)
    
    return org_name


if __name__ == "__main__":

    s = "3-T Forming North Inc."
    print(clean_org_name(s))

    # s = 'P.A.T.H Davey Home'
    # print(clean_org_name(s))

    # s =  'P. A. T. H. Davey Home'
    # print(clean_org_name(s))

    # s= 'corporation of the municipality of chatham-kent'
    # print(clean_org_name(s))
