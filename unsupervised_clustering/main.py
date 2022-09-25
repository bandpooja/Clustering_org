import re
import string


abber = ['PB is hot', 'P.B. is hot', 'P B is hot', 'P. B. is hot']
for s in abber:
    s = s.lower()
    pattern = '^[.+a-z+.|\w+a-z+\w|\w+a-z+.]'
    result = re.findall(pattern, s)
    print(result)