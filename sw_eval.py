import nltk 
import csv
from collections import Counter,defaultdict
import ast
import gender_guesser.detector as gender
import os
'''nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
'''


def safe_literal_eval(value):
    if not value or not value.strip():
        return []          
    return ast.literal_eval(value)

#Needed to modify some text files to make it so that it works properly haha

def strip_number_and_name(line):
  
    parts = line.split('"')
   
    if len(parts) >= 6:
        return parts[5].strip()
    else:
        return line.strip()  # fallback if format unexpected




def modify(file):
    new_lines = []
    new_file = os.path.join(os.path.dirname(file), "new_" + os.path.basename(file))
    with open(file, "r", encoding="utf-8") as fin, \
        open(new_file, "w", encoding="utf-8") as fout:
        L=fin.readlines()
        for i in range(1,len(L)):
            line = strip_number_and_name(L[i])
            fout.write(line + "\n")       # add newline
            new_lines.append(line)  

  
    os.replace(new_file, file)

#modify("sw4.txt")
#modify("sw5.txt")
#modify('sw6.txt')



with open('/cal/exterieurs/cmartin-24/Desktop/dogwhistle/data_complete_clean.csv') as datacsv:
    cols=csv.reader(datacsv,delimiter=';')
    header=next(cols)

oeuvres=defaultdict(int)

with open('/cal/exterieurs/cmartin-24/Desktop/dogwhistle/data_complete_clean.csv', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f,delimiter=";")
    for ligne in reader:
        oeuvres[ligne["title_oeuvre"]] += 1

#print(header)
#print(oeuvres)
def get_ships_sw():
    values = []
    relationships=[]
    models=['F/M','M/M','F/F']
    with open('/cal/exterieurs/cmartin-24/Desktop/dogwhistle/data_complete_clean.csv', newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f,delimiter=";")
        for ligne in reader:
            if ligne["title_oeuvre"]=='Star Wars - All Media Types':
            
                relationships.append([safe_literal_eval(ligne["relationship tags"]),safe_literal_eval(ligne['character tags']),safe_literal_eval(ligne['category tags']),safe_literal_eval(ligne['published'])])

    return relationships

Characters = defaultdict(int)


from collections import defaultdict
from copy import deepcopy
import pandas as pd

def build_df_sw(relationships):
    current_counts_sw = defaultdict(int)

    timeline_sw= {}

    relationships_sorted_sw = sorted(relationships, key=lambda x: x[3]) 

    for ships, chars, types, published in relationships_sorted_sw:


        for s in ships:
            current_counts_sw[s] += 1

        timeline_sw[published] = deepcopy(current_counts_sw)


    df_sw = pd.DataFrame.from_dict(timeline_sw, orient="index")

    df_sw = df_sw.sort_index().fillna(method="ffill").fillna(0)

    return df_sw

def get_stats_sw():

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
    with open("sw4.txt", "r", encoding="utf-8") as f1:
        sw4 = f1.read()
    sw4_tokens=nltk.word_tokenize(sw4)
    sw4_tags=nltk.pos_tag(sw4_tokens)

    with open("sw5.txt", "r", encoding="utf-8") as f2:
        sw5 = f2.read()
    sw5_tokens=nltk.word_tokenize(sw5)
    sw5_tags=nltk.pos_tag(sw5_tokens)

    with open("sw6.txt", "r", encoding="utf-8") as f3:
        sw6 = f3.read()
    sw6_tokens=nltk.word_tokenize(sw6)
    sw6_tags=nltk.pos_tag(sw6_tokens)


    corpus_tags=sw4_tags+sw5_tags+sw6_tags
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



"""résults for the 3 star wars movies:

{'F/M': 11, 'M/M': 2})
{'neutral_pronoun': 716, 'fem_pronoun': 105, 'masc_pronoun': 380})
{'female_characters': 10, 'neutral_characters': 106, 'male_characters': 12})
{'neutral_characters': 395, 'female_characters': 10, 'male_characters': 19})


cannon and heavily implied relation ships

F/M: Anakin/Padmé, Shmi/Cliegg, Han/Leia

c'est TOUT dans TOUT les films !!!!!!




"""
