import numpy as np
import re
import spacy
from bs4 import BeautifulSoup
from spacy.lang.en import English
from zipfile import ZipFile

tokenIndex = dict()
index = 0
for line in open("vocabulary.dat", "r"):
    value = line.strip("\r\n").split("\t")
    tokenIndex[value[1]] = index
    index = index + 1

vocabularySize = index

nlp = English()
tokenizer = nlp.tokenizer

size = dict()
size["trn"] = 10322
size["val"] = 1290
size["tst"] = 1290
with ZipFile("ml530-2021-sp-reuters.zip", "r") as archive:
    for partition in [ "trn", "val", "tst" ]:
        docCount = size[partition]
        docTokenMatrix = np.zeros((docCount, vocabularySize)).astype("float32")
        if (partition != "tst"):
            docLabelMatrix = np.zeros((docCount, 3)).astype("float32")
        index = 0
        for i in range(docCount):
            with archive.open("reuters_" + partition + "/reuters_" + partition + "_" + str(i).zfill(5) + ".sgm") as file:
                text = file.read().decode("utf-8")
                soup = BeautifulSoup(text, "html.parser")
                for element in [ soup.title, soup.body ]:
                    if (element != None):
                        temp = element.get_text()
                        temp = re.sub("[\t\r\n]", " ", temp)
                        temp = " ".join(temp.split())
                        for token in [ token.text for token in tokenizer(temp) ]:
                            key = token.lower()
                            if (key in tokenIndex):
                                docTokenMatrix[index, tokenIndex[key]] = 1
                if (partition != "tst"):
                    if (soup.topics != None):
                        labels = [ topic.get_text() for topic in soup.topics.find_all('d') ]
                    if ("earn" in labels):
                        docLabelMatrix[index, 0] = 1
                    if ("acq" in labels):
                        docLabelMatrix[index, 1] = 1
                    if ("money-fx" in labels):
                        docLabelMatrix[index, 2] = 1
            index = index + 1

        np.save("reuters_" + partition + "X.npy", docTokenMatrix)
        if (partition != "tst"):
            np.save("reuters_" + partition + "Y.npy", docLabelMatrix)
