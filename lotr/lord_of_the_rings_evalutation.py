import nltk 
import csv
from collections import Counter,defaultdict
import ast
import gender_guesser.detector as gender
'''nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
'''


def safe_literal_eval(value):
    if not value or not value.strip():
        return []          
    return ast.literal_eval(value)



values = []
relationships=[]
models=['F/M','M/M','F/F']
with open('/cal/exterieurs/cmartin-24/Desktop/dogwhistle/data_complete_clean.csv', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f,delimiter=";")
    for ligne in reader:
        if ligne["title_oeuvre"]=='TOLKIEN J. R. R. - Works & Related Fandoms':
          
            relationships.append([safe_literal_eval(ligne["relationship tags"]),safe_literal_eval(ligne['character tags']),safe_literal_eval(ligne['category tags'])])


Characters=defaultdict(int)
Ship=defaultdict(int)
RelationShipType=defaultdict(int)
for k in relationships:
    for i in k[1]:
        Characters[i]+=1
    for j in k[0]:
        Ship[j]+=1
    for h in models:
        if h in k[2]:
            RelationShipType[h]+=1
    

    
#print(relationships)

print(Characters)
print(Ship)
print(RelationShipType)




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
with open("lotr1.txt", "r", encoding="latin-1") as f1:
    lotr1 = f1.read()
lotr1_tokens=nltk.word_tokenize(lotr1)
lotr1_tags=nltk.pos_tag(lotr1_tokens)

with open("lotr2.txt", "r", encoding="latin-1") as f2:
    lotr2 = f2.read()
lotr2_tokens=nltk.word_tokenize(lotr2)
lotr2_tags=nltk.pos_tag(lotr2_tokens)

with open("lotr3.txt", "r", encoding="latin-1") as f3:
    lotr3 = f3.read()
lotr3_tokens=nltk.word_tokenize(lotr3)
lotr3_tags=nltk.pos_tag(lotr3_tokens)

with open("hobbit.txt", "r", encoding="latin-1") as f4:
    hobbit = f4.read()
hobbit_tokens=nltk.word_tokenize(hobbit)
hobbit_tags=nltk.pos_tag(hobbit_tokens)

corpus_tags=lotr1_tags+lotr2_tags+lotr3_tags+hobbit_tags
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

print(how_many_pronouns)
print(gendered_characters)
print(gendered_characters_canon)

"""résultats pour les livres de l'univers du seigneur des anneaux:
{'F/M': 7, 'M/M': 15, 'F/F': 1})
{'neutral_pronoun': 18871, 'masc_pronoun': 18486, 'fem_pronoun': 917})
{'neutral_characters': 67, 'male_characters': 6, 'female_characters': 10})
{'neutral_characters': 2389, 'female_characters': 58, 'male_characters': 89})"""