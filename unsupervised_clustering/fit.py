
import string



s= 'f. j. davey home'
s= s.translate(str.maketrans('', '', string.punctuation))
word=''
s= s.split(' ')
for idx, i in enumerate(s):
    if len(i) == 1:
        word+=i
        s.remove(idx)

print(word)

