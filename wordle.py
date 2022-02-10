#!/usr/bin/env python
# coding: utf-8


#%%

import pandas as pd
import time
from utils import get_language, get_df, get_wordlenght, update_df, get_input, word_recommendation, update_lists

print('\n************************************************************************************************************')
print('************************************************************************************************************')
print('********************************************** WORDLE SOLVER ***********************************************')
print('************************************************ by cayondo ************************************************')
print('************************************************************************************************************')
print('************************************************* v.1.0.0.1 ************************************************')
print('************************************************************************************************************')
print('************************************************************************************************************')
print('\nInstructions: After entering a word, type the outcome for every letter. Type 2 for green, 1 for yellow,\nand 1 for gray. To confirm the letter outcomes type 1, y, Y, Yes, or yes.\n')


df, n = get_df()
df_bk = df.copy()
alphabet, letters_used, exact_letters, sure_letters, impossible_letters = [],[],[],[],[]
for k in range(n): alphabet = alphabet+[x for x in list(df['letter_'+str(k+1)].unique()) if x not in alphabet]
alphabet.sort()
possible_letters = [x for x in alphabet]
somwhere_letter = {x:[] for x in alphabet}
limit = 10

for turn in range(1,7):            

    print('\n\nTurn '+str(turn),' - ','Possible words left:',len(df),'\n')

    if len(df)==1:
        
        print('Solution found:',df.iloc[0]['word'])
        time.sleep(5)
        break

    elif len(df)>1:
        
        print('Possible letters:',possible_letters)
        print('Impossible letters:',impossible_letters,'\n')

        if len(df)<=limit: 
        	words_left = list(df.sort_values('score',ascending=False)['word'])
        	print('Possible words:',words_left)
        if len(df) == 2: 
        	print('Recommended word:',words_left[0])
        else:
        	words_recommended = word_recommendation(df_bk,possible_letters,sure_letters,exact_letters)
        	print('Recommended word:',words_recommended[0])


        word, word_result = get_input(n,alphabet)
        letters_used = list(set(letters_used + list(word)))
        df = update_df(df,word_result)
        possible_letters,impossible_letters,sure_letters,somwhere_letter,exact_letters = update_lists(df,word_result,alphabet,possible_letters,impossible_letters,sure_letters,somwhere_letter,exact_letters)       

    elif len(df)==0:
        print('No solution - check for errors in input and try again')
        break



