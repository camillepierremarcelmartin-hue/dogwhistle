import nltk 
import csv
from collections import Counter,defaultdict
import ast
import gender_guesser.detector as gender
from datetime import datetime,date,timedelta
'''nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
'''


def safe_literal_eval(value):
    if not value or not value.strip():
        return []          
    return ast.literal_eval(value)


with open('data_complete_clean.csv') as datacsv:
    cols=csv.reader(datacsv,delimiter=';')
    header=next(cols)

def get_ships_hp():
    values = []
    relationships=[]
    models=['F/M','M/M','F/F']
    with open('data_complete_clean.csv', newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f,delimiter=";")
        for ligne in reader:
            if ligne["title_oeuvre"]=='Harry Potter - J. K. Rowling':
            
                relationships.append([safe_literal_eval(ligne["relationship tags"]),safe_literal_eval(ligne['character tags']),safe_literal_eval(ligne['category tags']),safe_literal_eval(ligne['published'])])

    return relationships

Characters = defaultdict(int)


from collections import defaultdict
from copy import deepcopy
import pandas as pd

def build_df_hp(relationships):

    current_counts_hp = defaultdict(int)

    timeline_hp= {}

    relationships_sorted_hp = sorted(relationships, key=lambda x: x[3]) 

    for ships, chars, types, published in relationships_sorted_hp:


        for s in ships:
            current_counts_hp[s] += 1

        timeline_hp[published] = deepcopy(current_counts_hp)


    df_hp = pd.DataFrame.from_dict(timeline_hp, orient="index")

    df_hp = df_hp.sort_index().fillna(method="ffill").fillna(0)
    
    return df_hp





def get_stats_hp():

    d=gender.Detector()
    gen=d.get_gender("Vader")
    print(gen)
    gendered_characters=defaultdict(int)
    for k in Characters.keys():
        name=k.split(" ")[0]
        gen=d.get_gender(name)
        if gen in ['male','mostly_male']:
            gendered_characters['male_characters']+=1
        elif gen in ['female','mostly_female']:
            gendered_characters['female_characters']+=1
        else:
            gendered_characters['neutral_characters']+=1

    masc = ["he", "him", "his", "himself"]
    fem=["she","her","hers","herself"]
    neut=["they", "them", "their", "theirs", "themself", "themselves","it"]
    type_of_pronouns=["PRP","PRP$"]

    how_many_pronouns=defaultdict(int)
    gendered_characters_canon=defaultdict(int)
    with open("harrypotter1.txt", "r", encoding="utf-8") as f1:
        hp1 = f1.read()
    hp1_tokens=nltk.word_tokenize(hp1)
    hp1_tags=nltk.pos_tag(hp1_tokens)

    with open("harrypotter2.txt", "r", encoding="utf-8") as f2:
        hp2 = f2.read()
    hp2_tokens=nltk.word_tokenize(hp2)
    hp2_tags=nltk.pos_tag(hp2_tokens)

    with open("harrypotter3.txt", "r", encoding="utf-8") as f3:
        hp3 = f3.read()
    hp3_tokens=nltk.word_tokenize(hp3)
    hp3_tags=nltk.pos_tag(hp3_tokens)

    with open("harrypotter4.txt", "r", encoding="utf-8") as f4:
        hp4 = f4.read()
    hp4_tokens=nltk.word_tokenize(hp4)
    hp4_tags=nltk.pos_tag(hp4_tokens)

    with open("harrypotter5.txt", "r", encoding="utf-8") as f5:
        hp5 = f5.read()
    hp5_tokens=nltk.word_tokenize(hp5)
    hp5_tags=nltk.pos_tag(hp5_tokens)

    with open("harrypotter6.txt", "r", encoding="utf-8") as f6:
        hp6 = f6.read()
    hp6_tokens=nltk.word_tokenize(hp6)
    hp6_tags=nltk.pos_tag(hp6_tokens)

    with open("harrypotter7.txt", "r", encoding="utf-8") as f7:
        hp7 = f7.read()
    hp7_tokens=nltk.word_tokenize(hp7)
    hp7_tags=nltk.pos_tag(hp7_tokens)
    corpus_tags=hp1_tags+hp2_tags+hp3_tags+hp4_tags+hp5_tags+hp6_tags+hp7_tags
    character_list_cannon=[]
    i=0
    while i < len(corpus_tags):
        if corpus_tags[i][1] in type_of_pronouns:
            w = corpus_tags[i][0].lower().strip(".,!?\"'")

            if w in masc:
                how_many_pronouns['masc_pronoun']+=1
            elif w in fem:
                how_many_pronouns['fem_pronoun']+=1
            elif w in neut:
                how_many_pronouns["neutral_pronoun"]+=1
        if corpus_tags[i][1]=="NNP":
            if corpus_tags[i+1][1]=="NNP":  
                corpus_tags[i]= (corpus_tags[i][0]+" "+corpus_tags[i+1][0], "NNP")
                corpus_tags.pop(i+1)
            name=corpus_tags[i][0].split(" ")[0]
            if name.lower().strip(".,!?\"'") not in character_list_cannon:
                character_list_cannon.append(name.lower().strip(".,!?\"'"))
                gen=d.get_gender(name)
                if gen in ['male','mostly_male']:
                    gendered_characters_canon['male_characters']+=1
                elif gen in ['female','mostly_female']:
                    gendered_characters_canon['female_characters']+=1
                else:
                    gendered_characters_canon['neutral_characters']+=1
        i+=1

    return how_many_pronouns,gendered_characters,gendered_characters_canon
"""Résultats pour Harry Potter
{'neutral_pronoun': 27795, 'masc_pronoun': 44252, 'fem_pronoun': 10758})
{'male_characters': 37, 'neutral_characters': 39, 'female_characters': 25})
{'neutral_characters': 4315, 'male_characters': 254, 'female_characters': 159})


cannon and heavily implied relation ships

F/M: Harry/Ginny, Ron/Hermione, Bill/Fleur, Remus/Tonks, James/Lily, Andromeda/Ted, Narcissa/Lucius (heavily implied)
M/M: Dumbledore/Grindelwald (heavily implied)

"""
