import re

def remove_abbreviation(org_name: str):
    org_name = org_name.lower()

    org_words = org_name.split(' ')
    org_words_w_aggregated_abb = []
    for w in org_words:
        if len(w) == 1:
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

if __name__ == "__main__":
    s = 'P A T H Davey Home'
    print(remove_weird_characters(remove_abbreviation(s)))

    s = 'P.A.T.H Check check'
    print(remove_weird_characters(remove_abbreviation(s)))

    s =  'P. A. T. H. Check check'
    print(remove_weird_characters(remove_abbreviation(s)))
