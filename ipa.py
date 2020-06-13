from glob import glob
from nltk import bigrams
from collections import defaultdict
import re, os
import pickle

def process_raw_ipa_files():
    source_path = "../ipa-dict/data/{}.txt"
    target_path = "../resources/lang/{}.txt"

    lengths = re.compile(r'(.)([:ː])', re.I)
    flatten = lambda term : lengths.sub(r'\1\1', term)

    insides = re.compile(r'/(.+?)/', re.I)
    extract = lambda text : insides.findall(text)

    for lang in glob(source_path.format("*")):
        with open(lang) as fin:
            text = flatten(fin.read())
            text = extract(text)

            with open(f'./resources/lang/{os.path.basename(lang)}.txt', 'w') as fout:
                output = '\n'.join(text)
                fout.write(output)


def remove_stress_marks(text):
    primary, secondary = "ˈ", "ˌ"
    return text.replace(primary, "").replace(secondary, "")


def count_bigrams(text, model=None):
    if model:
        pass
    else:
        model = defaultdict(dict)
    
    for (A, B) in bigrams(text):
        model[A].setdefault(B, 0)
        model[A][B] += 1

    return model


if __name__ == "__main__":
    with open("./resources/lang/all/all.txt") as fin:
        model = defaultdict(dict)
        for line in fin.readlines():
            line = line.strip()
            model count_bigrams(line, model)
    

    pickle.dump(model, open("resources/lang/counts.pkl", "wb"))
            