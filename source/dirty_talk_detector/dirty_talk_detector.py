import math
import re
import os.path
from nltk.stem.snowball import SnowballStemmer

path_weight = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secretData.csv')

map_idf = {}

b_0 = -6.907789551823112

IS_FILE = os.path.isfile(path_weight)

if IS_FILE:
    f = open(path_weight, "r", encoding="utf-8")

    i = 0
    for line in f:
        if i == 0:
            i = i + 1
            continue
        word, weight = line.split(",")
        map_idf[word] = float(weight)
        i = i + 1
    f.close()
    stemmer = SnowballStemmer("russian")


def sigmoid(x):
    return 1 / (1 + math.exp((-1) * x))


def detect(s):
    if not IS_FILE:
        return 0

    s = re.sub(r'[^\w]', ' ', s)
    arr = s.split(" ")
    summ = 0
    for n in arr:
        try:
            summ = summ + map_idf[stemmer.stem(n.lower())]
        except:
            continue
    return sigmoid(summ + b_0)
