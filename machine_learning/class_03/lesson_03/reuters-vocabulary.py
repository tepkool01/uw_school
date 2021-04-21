import numpy as np
import re
import spacy
from bs4 import BeautifulSoup
from spacy.lang.en import English
from zipfile import ZipFile

# To install the syntactic parser implemented in Cython (spaCy):
# pip install spacy
# python -m spacy download en_core_web_sm

# To install the Beautiful Soup HTML parser:
# pip install bs4

vocabularySize = 10000

#nlp = spacy.load("en_core_web_sm")
#tokenizer = English().Defaults.create_tokenizer(nlp)
nlp = English()
tokenizer = nlp.tokenizer

# create token-to-file mapping
mapping = dict()
with ZipFile("ml530-2021-sp-reuters.zip", "r") as zip:
    index = 0
    for i in range(10322):
        with zip.open("reuters_trn/reuters_trn_" + str(i).zfill(5) + ".sgm") as file:
            text = file.read().decode("utf-8")
            soup = BeautifulSoup(text, "html.parser")
            for element in [ soup.title, soup.body ]:
                if (element != None):
                    temp = element.get_text()
                    temp = re.sub("[\t\r\n]", " ", temp)
                    temp = " ".join(temp.split())
                    for token in [ token.text for token in tokenizer(temp) ]:
                        key = token.lower()
                        if (key not in mapping):
                            mapping[key] = set()
                        if (i not in mapping[key]):
                            mapping[key].add(i)
        index = index + 1

# create frequency-to-token mapping
members = dict()
for k,v in mapping.items():
    freq = len(v)
    if (freq not in members):
        members[freq] = []
    if (k not in members[freq]):
        members[freq].append(k)

# sort tokens by frequency, in descending order
tuples = sorted(members.items(), reverse = True)
if (vocabularySize > len(mapping)):
    vocabularySize = len(mapping)

# select most frequent tokens for the vocabulary
selected = []
needed = vocabularySize
for i in range(len(tuples)):
    if (needed > 0):
        candidates = tuples[i][1]
        np.random.shuffle(candidates)
        count = len(candidates)
        if (count > needed):
            for j in range(needed):
                selected.append(candidates[j])
                needed = needed - 1
        else:
            for candidate in candidates:
                selected.append(candidate)
                needed = needed - 1
    else:
        break

# write out vocabulary
output = open("vocabulary.dat", "w")
for token in selected:
    output.write(str(len(mapping[token])) + "\t" + token + "\n")
output.close()
