import pandas as pd
from utils import get_language, get_wordlenght, get_encoding

language = get_language()
number = get_wordlenght()
vowels = ['a','e','i','o','u']
encoding = get_encoding(language)

df = pd.read_csv('words_'+language+'_'+str(number)+'.csv',encoding=encoding)
freq = pd.read_csv('frequency_'+language+'.csv',encoding=encoding).sort_values('letter')
alphabet = list(freq['letter'])
alphabet.sort()

for l in alphabet: df[l] = [1 if l in x else 0 for x in df['word']]
for k in range(5): df['letter_'+str(k+1)] = [x[k] for x in df['word']]
df['unique'] = [len(set(x)) for x in df['word']]
df['vowels'] = df[vowels].sum(axis=1)
df['score'] = 0
for l in alphabet: df['score'] = df['score']+df[l]*freq[freq.letter==l]['frequency'].iloc[0]

df.to_csv('scores_'+language+'_'+str(number)+'.csv',index=False, encoding=encoding)