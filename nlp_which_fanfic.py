import nltk 
import csv
from collections import Counter
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

s="he she they them her their him it"

tokens=nltk.word_tokenize(s)
#print(tokens)

tagged=nltk.pos_tag(tokens)
#print(tagged)

with open('data_complete_clean.csv') as datacsv:
    cols=csv.reader(datacsv,delimiter=';')
    header=next(cols)
    
print(header)




values = []

with open('data_complete_clean.csv', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f,delimiter=";")
    for ligne in reader:
        values.append(ligne["title_oeuvre"])


count = Counter(values)
valeur_max, nb_max = count.most_common(1)[0]
D_OE=dict(count)
print(valeur_max)

print("Valeur la plus fréquente :", valeur_max)
print("Nombre d'occurrences :", nb_max)