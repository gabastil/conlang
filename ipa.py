from glob import glob
from nltk import bigrams
from sounds import Consonant, Vowel
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
    
    for (A, B) in bigrams(f"^{text}$"):
        model[A].setdefault(B, 0)
        model[A][B] += 1

    return model


def count_unigrams(text, model=None):
    ''' Count the occurrence of individual characters in a text '''
    if model:
        pass
    else:
        model = defaultdict(int)
    
    for A in text:
        model[A] += 1
    
    return model


def get_feature_distributions(data, features, feature_values):
    ''' Get distributions of features and their values '''

    def feature_set(feature, data, consonant=True):
        return [Consonant(char) if consonant else Vowel(char) for char, count in data]

    def feature_counts(features, values):
        counts = []
        for value in values:
            filtered = filter(lambda t: t[0] == value, features)
            total_count = sum([b for a, b in filtered])
            counts.append((value, total_count))
        return counts

    distribution = []

    for i, feature in enumerate(features):
        set_ = feature_set(feature, data)
        cts_ = feature_counts(set_, feature_values[i])
        p = cts_ / cts_.sum()
        distribution.append(p)
    
    return distribution



if __name__ == "__main__":
    with open("./resources/lang/all/all.txt") as fin:
        # print(fin.read()[:100])
        model = None
        for line in fin.readlines():
            line = line.strip()
            # model = count_unigrams(line, model)
            model = count_bigrams(line, model)
        
        print(model)
        pickle.dump(model, open("./resources/lang/all/bigrams.pkl", "wb"), protocol=3)
    

    # pickle.dump(model, open("resources/lang/counts.pkl", "wb"))
            