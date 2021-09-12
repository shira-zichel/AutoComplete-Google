from itertools import combinations
from string import ascii_lowercase
import re
import os


sentences_list = []
dict = {}
scores = {}


class AutoCompleteData:
    def __init__(self, complete_sentence, source_text):
        self.m_complete_sentence = complete_sentence
        self.m_source_text = source_text

    def __str__(self):
        return "\nsen is: %s\nfile is: %s" %(self.m_complete_sentence, self.m_source_text)

    def __repr__(self):
        return "\nsen is: %s\nfile is: %s" %(self.m_complete_sentence, self.m_source_text)


def initial_file(file_name):
    with open(file_name, mode='r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[%!@#/$*"().\n]', '', line)
            line = line.strip()
            if line == '':
                continue
            a = AutoCompleteData(line, file_name)
            sentences_list.append(a)
            index = len(sentences_list) - 1
            #print(line)
            words = line.split(' ')
            #print(words)
            prefix_combinations = [words[x:y] for x, y in combinations(range(len(words) + 1), r=2)]
            #print(prefix_combinations)
            for word in prefix_combinations:
                word = ' '.join(word)
                if word not in dict:
                    dict[word] = []
                dict[word].append(index)
                #if len(dict[word])<5:
                #    dict[word].append(index)
    return dict


def search(input):
    if input in dict:
        if len(dict[input])>=5:
            sorted_list = order(dict[input])
            for item in sorted_list[:5]:
                print(sentences_list[item])
            return

    scores = {}
    insert(input, scores)
    replace(input, scores)
    erase(input, scores)
    #sort by scores
    scores = sort_scores(scores)
    #group to scores
    res = {}
    for i, v in scores.items():
        res[v] = [i] if v not in res.keys() else res[v] + [i]
    #sort alpha-bet
    for k,v in res.items():
        res[k] = order(v)
    #take the first 5
    list = []
    for v in res.values():
        for i in v:
            list.append(i)
    #print the identical sentences
    sum = 5
    if input in dict:
        sorted_index = order(dict[input])
        for item in sorted_index:
            print(sentences_list[item])
            sum = 5 - len(dict[input])
    s = sum
    for k,v in res.items():
        for i in v:
            if s == 0:
                break
            print(sentences_list[i], "\nscore:" ,k, " offset:")
            s -= 1


#sort dictionary by scores
def sort_scores(scores):
    return {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}


#get index and return the object
def get_object(index):
    return sentences_list[index]


#sort list by alpha-bet
def order(index):
    ordered_sentences={}
    for i in index:
        ordered_sentences[i]=(get_object(i).m_complete_sentence)
    new_ordered_sentences={k: v for k, v in sorted(ordered_sentences.items(), key=lambda item: item[1])}
    indexes_list=[]
    for item in new_ordered_sentences:
        indexes_list.append(item)
    return indexes_list


#punishments for replace
def punishments(index):
    d = {1:5,2:4,3:3,4:2}
    if index>=5:
        return 1
    else:
        return d[index]


def replace(word, scores):
    index = 1
    for i in word:
        for l in ascii_lowercase:
            w = word.replace(i,l)
            if w != word:
                if w in dict:
                    score = (len(word)-1)*2-punishments(index)
                    for s in dict[w]:
                        scores[s] = score
        index += 1


def insert(word, scores):
    for index in range(len(word)+1):
        for l in ascii_lowercase:
            new_string = word[:index] + l+ word[index:]
            if new_string in dict:
                if index>3:
                    score=len(word)*2-2
                elif index==0:
                    score=len(word)*2-10
                elif index==1:
                    score=len(word)*2-8
                elif index==2:
                    score=len(word)*2-6
                elif index==3:
                    score=len(word)*2-4
                for s in dict[new_string]:
                    scores[s] = score


def erase(word, scores):
    for index in range(len(word)):
        new_string=word[:index] + word[index + 1:]
        if new_string in dict:
            if index > 3:
                score = len(word)*2 - 2
            elif index == 0:
                score = len(word)*2 - 10
            elif index == 1:
                score = len(word)*2 - 8
            elif index == 2:
                score = len(word)*2 - 6
            elif index == 3:
                score = len(word)*2 - 4
            for s in dict[new_string]:
                scores[s] = score



#initial
rootdir = r"C:\שנה ג סמס ב\בוטקאמפ\2021-archive\2021-archive"
for subdir, dirs, files in os.walk(rootdir):
   for file in files:
        initial_file(os.path.join(subdir, file))

#search
word=""
while word!='#':
    word = input("Enter a word: ")
    search(word)

