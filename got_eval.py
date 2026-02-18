import nltk 
import csv
from collections import Counter,defaultdict
import ast
import gender_guesser.detector as gender
from copy import deepcopy
import pandas as pd
'''nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
'''


def safe_literal_eval(value):
    if not value or not value.strip():
        return []          
    return ast.literal_eval(value)

def normalize_ship(ship):
    chars = sorted([c.strip() for c in ship.split("/")])
    return "/".join(chars)


def get_ships_got():
    values = []
    relationships=[]
    models=['F/M','M/M','F/F']
    with open('/cal/exterieurs/cmartin-24/Desktop/dogwhistle/data_complete_clean.csv', newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f,delimiter=";")
        for ligne in reader:
            if ligne["title_oeuvre"]=='A Song of Ice and Fire & Related Fandoms':
            
                relationships.append([safe_literal_eval(ligne["relationship tags"]),safe_literal_eval(ligne['character tags']),safe_literal_eval(ligne['category tags']),safe_literal_eval(ligne["published"])])
    return relationships

Characters = defaultdict(int)


def build_df_got(relationships):


    current_counts_got = defaultdict(int)

    timeline_got= {}

    relationships_sorted_got = sorted(relationships, key=lambda x: x[3]) 

    for ships, chars, types, published in relationships_sorted_got:

        if isinstance(published, list):
            published = published[0]


        for s in ships:
            s_n=normalize_ship(s)
            current_counts_got[s_n] += 1

        timeline_got[published] = deepcopy(current_counts_got)


    df_got = pd.DataFrame.from_dict(timeline_got, orient="index")

    df_got = df_got.sort_index().ffill().fillna(0)

    return df_got


def get_stats_got(relationships):
    unique_ships = set()

    for ships, chars, types, published in relationships:
        for ship in ships:
            unique_ships.add(normalize_ship(ship))

    ship_to_characters = {}

    for ship in unique_ships:
        characters = [c.strip() for c in ship.split("/")]
        ship_to_characters[ship] = characters

    type_counts = defaultdict(int)

    for ships, chars, types, published in relationships:
        for t in types:
            type_counts[t] += 1

   
    for t, count in type_counts.items():
        print(f"{t} : {count}")
    d=gender.Detector()
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
    with open("got1.txt", "r", encoding="latin-1") as f1:
        got1 = f1.read()
    got1_tokens=nltk.word_tokenize(got1)
    got1_tags=nltk.pos_tag(got1_tokens)

    with open("got2.txt", "r", encoding="latin-1") as f2:
        got2 = f2.read()
    got2_tokens=nltk.word_tokenize(got2)
    got2_tags=nltk.pos_tag(got2_tokens)

    with open("got3.txt", "r", encoding="latin-1") as f3:
        got3 = f3.read()
    got3_tokens=nltk.word_tokenize(got3)
    got3_tags=nltk.pos_tag(got3_tokens)

    with open("got4.txt", "r", encoding="latin-1") as f4:
        got4 = f4.read()
    got4_tokens=nltk.word_tokenize(got4)
    got4_tags=nltk.pos_tag(got4_tokens)

    with open("got5.txt", "r", encoding="latin-1") as f5:
        got5 = f5.read()
    got5_tokens=nltk.word_tokenize(got5)
    got5_tags=nltk.pos_tag(got5_tokens)

    corpus_tags=got1_tags+got2_tags+got3_tags+got4_tags+got5_tags
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


    return how_many_pronouns, gendered_characters, gendered_characters_canon,unique_ships,ship_to_characters,type_counts



"""got sur le bon dieu"""
