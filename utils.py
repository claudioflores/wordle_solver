import pandas as pd


def get_df():

    language = get_language()
    n = get_wordlenght()
    encoding = get_encoding(language)
    file_name = 'scores_'+language+'_'+str(n)+'.csv'
    
    try:
        df = pd.read_csv(file_name, encoding=encoding)
    except:
        print('\nWord dictionary not found, try again\n')
        df,n = get_df()

    return df,n


def get_language():
    languages = ['english','spanish']
    language = input('Select language: '+str(languages)+': ')
    if language not in languages:
        language = get_language()
    return language

def get_encoding(language):
    if language == 'spanish': return 'latin-1'
    elif language == 'english': return 'utf-8'

def get_wordlenght():    
    number = input('What is the lenght of the word: ')
    try:
        number = int(number)
        if number<1:
            print('Input needs to be a positive integer, please try again')
            number = get_wordlenght()    
    except:
        print('Input is not a integer, please try again')
        number = get_wordlenght()            
    return number

def get_letterresult(letter):    
    result = input('Result letter "'+letter+'" ? ')
    if result in ['0','1','2']:
        return result        
    else:
        print('Error in input, please write 0, 1, or 2')
        result = get_letterresult(letter)    
    return result

def get_word(n,alphabet):    
    word = input('Enter word: ')    
    if len(word) != n:
        print('Word does not have the right lenght, please try again')
        word = get_word(n,alphabet)        
    for letter in word:
        if letter not in alphabet:
            print('One of the characters is not in the alphabet, please try again')
            word = get_word(n,alphabet)            
    return word

def get_results(word,n,alphabet):    
    word_result = pd.DataFrame(columns=['letter','result']).copy()    
    for letter in word:
        word_result.loc[len(word_result)] = [letter,get_letterresult(letter)]     
    finish = input('Final solution? ')    
    if finish not in ('1','y','Y','Yes','yes','YES'):
        word, word_result = get_input(n,alphabet)

    aux = word_result.groupby('letter').agg({'result':['max']}).reset_index()
    aux.columns = ['letter','max']
    word_result = word_result[['letter','result']].merge(aux,on='letter',how='left')
    word_result['order'] = word_result.index+1 

    return word, word_result

def get_input(n,alphabet):    
    word = get_word(n,alphabet)    
    word,word_result = get_results(word,n,alphabet)    
    return word, word_result

def update_df(df,word_result):
    
    df0 = df.copy()

    for index, row in word_result.iterrows():

        order = row['order']
        letter = row['letter']
        result = int(row['result'])
        maxv = int(row['max'])

        if result == 0:
            df0 = df0[df0['letter_'+str(order)]!=letter]

            if maxv == 0:
                df0 = df0[df0[letter]==0]

            if maxv == 2:
                aux_list = list(word_result[(word_result['letter']==letter)&(word_result['result']=='2')]['order'])
                for k in range(5):
                    order2 = k+1
                    if order2 not in [order]+aux_list:
                        df0 = df0[df0['letter_'+str(order2)]!=letter]                    

        elif result == 1:
            df0 = df0[df0[letter]==1]
            df0 = df0[df0['letter_'+str(order)]!=letter]        

        elif result == 2:
            df0 = df0[df0['letter_'+str(order)]==letter]

    return df0


def word_recommendation(df0,possible_letters,sure_letters,exact_letters,limit=10):    
    df = df0.copy()
    letter_list = [x for x in sure_letters if x not in exact_letters]
    df['aux'] = df[possible_letters].sum(axis=1)
    df['aux2'] = df[letter_list].sum(axis=1)
    return list(df.sort_values(['aux','aux2','score'],ascending=[False,False,False])['word'].head(limit))


def update_lists(df,word_result,alphabet,possible_letters,impossible_letters,sure_letters,somwhere_letter,exact_letters):

    for index, row in word_result.iterrows():
            
        order = row['order']
        letter = row['letter']
        result = int(row['result'])
        maxv = int(row['max'])

        if (result == 0)&(maxv==0):
            if letter in possible_letters:
                possible_letters.remove(letter)
            if letter not in impossible_letters:
                impossible_letters.append(letter)
                impossible_letters.sort()

        if result in [1,2]:
            if letter not in sure_letters:
                sure_letters.append(letter)
                sure_letters.sort()
            if letter in possible_letters:
                possible_letters.remove(letter)
            if result == 1:
                if len(somwhere_letter[letter]) == 0:
                    somwhere_letter[letter] = [order]
                elif order not in somwhere_letter[letter]:
                    aux = somwhere_letter[letter]+[order] 
                    aux.sort
                    somwhere_letter[letter] = aux
            if result == 2:
                exact_letters.append(letter)

    for l in alphabet:
        if df[l].max()==0:
            if l in possible_letters:
                possible_letters.remove(l)
            if l not in impossible_letters:
                impossible_letters.append(l)
                impossible_letters.sort()

    return possible_letters,impossible_letters,sure_letters,somwhere_letter,exact_letters