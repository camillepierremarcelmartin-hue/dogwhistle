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
        return []          # or None, depending on what you want
    return ast.literal_eval(value)


s="he she they them her their him it"

tokens=nltk.word_tokenize(s)
print(tokens)

tagged=nltk.pos_tag(tokens)
#print(tagged)

with open('data_complete_clean.csv') as datacsv:
    cols=csv.reader(datacsv,delimiter=';')
    header=next(cols)
    
#print(header)




values = []
relationships=[]
models=['F/M','M/M','F/F']
with open('data_complete_clean.csv', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f,delimiter=";")
    for ligne in reader:
        if ligne["title_oeuvre"]=='Harry Potter - J. K. Rowling':
          
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

"""print(Characters)
print(Ship)
print(RelationShipType)"""



#For ease of work, we will use the harry potter books series, written by known transphobe and racist JK Rowling


with open("harrypotter1.txt", "r", encoding="utf-8") as f:
    hp1 = f.read()

