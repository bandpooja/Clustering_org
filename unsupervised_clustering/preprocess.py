import re


def remove_abbreviation(org_name: str):
    org_name = org_name.lower()
    # |(?:\s(a-z)\s)]
    pattern = r'(?:\.[a-z]\.|\s[a-z]\s|\.\s[a-z]\.)+'

    result = re.findall(pattern, org_name)
    if result:
        for r in result:
            pattern_w = r'(?:[a-z])'
            x = re.findall(pattern_w, r)
            if r[-1] == ' ':
                org_name = org_name.replace(r, x[0]+ ' ')
            else:
                org_name = org_name.replace(r, x[0])
    return org_name
