import re, csv

file = open('/home/hacky/Desktop/Applied-AI/Projects/Text2CSV/gre_vocab_text.txt', 'r', errors = 'replace')

dictionary = {}
key_words_list = []
key_meanings_list = []
key_eg_sentences_list = []
words_list = []
meanings_list = []
eg_sentences_list = []

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def hasNumbersDot(inputString):
    return bool(re.search(r'^((\d)+?(\.))', inputString))


# create a list of lines in the file

lines_list = file.readlines()

clean_lines_list = []
for line in lines_list:
    clean_line = line.replace('\n', '')
    clean_lines_list.append(clean_line)
    
for line in clean_lines_list:
    if line == '':
        del clean_lines_list[clean_lines_list.index(line)] #provide a string to find an index i.e. clean_lines_list.index('1. Angry')


# extract keys i.e. 1. Angry
matched_strings_list = []

for i, line in enumerate(clean_lines_list):
    if hasNumbersDot(line) == True:
        string = line
        index = string.index('.')
        
        # to modify strings like:
        # 104.                               
        # To accept/ give in/ agree
        if len(string[index+1:]) == 0:                              
            string = line + ' ' + clean_lines_list[i+1]
            matched_strings_list.append(string)
        else:
            matched_strings_list.append(line)

for i, line in enumerate(clean_lines_list):
    
    if '=' in line: # words and meanings extraction part
        string = line
        index = string.index('=')
        word = string[:index]
        meaning = string[index+1:]
        words_list.append(word)
        meanings_list.append(meaning)
        
    elif ':' in line: # extract examples
        string = line
        index = string.index(':')
        
        if i < 4428:
            if '=' not in clean_lines_list[i+1] and hasNumbers(clean_lines_list[i+1]) == False: 
                # for meanings > 1 lines 
                # i.e : Example: This is my
                #                name.
                    example = string[index+1:] + clean_lines_list[i+1]
                    eg_sentences_list.append(example)

            else: 
                example = string[index+1:]
                eg_sentences_list.append(example)

    elif hasNumbers(line) == True: # extract topics
        if i == 0:
            continue
        key_words_list.append(words_list)
        key_meanings_list.append(meanings_list)
        key_eg_sentences_list.append(eg_sentences_list)
        words_list = [] # reset all three lists for new key
        meanings_list = []
        eg_sentences_list = []    

# for dictionary key assignment
zipped_list = zip(key_words_list, key_meanings_list, key_eg_sentences_list)

refined_zipped_list = []

for tuples in zipped_list: # convert tuples into list
    litup = list(tuples)
    refined_zipped_list.append(litup)
    
values_list = []
for lists in refined_zipped_list: # unzips the corresponding values and return as a list
    values = list(zip(*lists))
    values_list.append(values)

for i in range(278): # 279 keys
    dictionary[matched_strings_list[i]] = values_list[i]
   
file.close()

with open('gre_vocab_csv.csv', 'w') as f:
    w = csv.writer(f, delimiter = ',')
    w.writerow(['TOPIC', 'WORD', 'MEANING', 'SENTENCE'])
    
    for Topic, Words in dictionary.items():
        for Word, Meaning, Sentence in Words:
            w.writerow([Topic, Word, Meaning, Sentence,])
            w.writerow('\n')
f.close()
