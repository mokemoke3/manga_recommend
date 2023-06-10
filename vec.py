import MeCab
import numpy as np
import ot
import fasttext
# import pandas as pd
import json
import pickle
from tqdm import tqdm

def get_w(text, mt, mdl):
    kws = mt.parse(text).split()
    # w = [np.array(wv[kw]) for kw in kws if kw in wv]
    w = [np.array(mdl.get_word_vector(' '.join(kw))) for kw in kws]
    return w

# ノルムの計算
def get_z(w):
    z = 0
    for w_i in w:
        z += np.linalg.norm(w_i)
    return z

# コストの計算
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



mt = MeCab.Tagger('-Owakati -d "C:/Program Files (x86)/MeCab/dic/ipadic" -u "C:/Program Files (x86)/MeCab/dic/ipadic/neologd.dic"')
wv = fasttext.load_model('wiki_comic.bin')
# uro_df = uro_df.reset_index()
# uro_df.to_csv('/home/project/uro_data_kensaku_drop.csv')
with open("./data/all.json", mode="r", encoding="utf8") as f:
    data = json.load(f)

w = []
m = []
for i in tqdm(data):
    w1 = get_w(data[i]["title"], mt, wv)
    w.append(w1)
    # print(w1)
    z1 = get_z(w1)
    m1 = [np.linalg.norm(w1_i) / z1 for w1_i in w1]
    
    m.append(m1)
    # break

with open("./data/vec.binaryfile", mode="wb") as f:
    pickle.dump(w, f)
with open("./data/norm.binaryfile", mode="wb") as f:
    pickle.dump(m, f)