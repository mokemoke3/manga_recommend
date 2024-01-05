import fasttext as ft
import MeCab
from gensim.summarization.bm25 import BM25
import numpy as np
import pickle
import ot
import json

class recommend:

    def __init__(self) -> None: 
        pass
    
    # 初期化 MeCabのTagger設定、モデルのロード
    def __init__(self):
        self.model = ft.load_model("./wiki_comic.bin")
        self.tagger = MeCab.Tagger('-Owakati')
        self.ids = load_pickle("./data/ids.binaryfile")
        self.json = load_json("./data/all.json")
        bm = best_match()
        self.bm = bm
        self.bm.pre_process()

    # 入力の前処理
    def input_txt(self, input):
        self.input = input
        self.wkt = self.tagger.parse(self.input)

    # BM25での検索
    def search_bm25(self):
        self.b = self.bm.ranking(self.input)
    
    # WRDで近しいものの検索
    def search_wrd(self):
        wrd = Word_Rotators(self.model, self.tagger, self.wkt, self.ids)
        self.c, self.i = wrd.calc()
    
    # 上位4件のデータ取得
    def rank(self, data, d_a):
        sort = np.argsort(data)
        # 降順に並び替え
        if d_a == "d":
            result = sort[-4:]
        # 昇順に並び替え
        elif d_a == "a":
            result = sort[:4]
        r_4 = {}
        for i, j in enumerate(result):
            r_4[str(i)] = self.json[self.ids[j]]
        return r_4
    
    def search(self):
        search_b = self.rank(self.b, "d")
        search_c = self.rank(self.c, "a")
        search_i = self.rank(self.i, "a")
        search_r = self.rank(self.c, "d")
        return search_b, search_c, search_i, search_r
        
        

# BM25の検索
# 参考 https://qiita.com/Lucky_Acky/items/9fbbd4b23c28a5c8622f
class best_match:

    def __init__(self):
        self.tagger = MeCab.Tagger('-Owakati')
    #前処理
    def pre_process(self):
        self.docs = load_pickle("./data/all.binaryfile")
        self.bm25_ = BM25(self.docs)
    
    #クエリとの順位付け
    def ranking(self, query):
        wakachi_query = self.wakachi(query)
        self.scores = self.bm25_.get_scores(wakachi_query)
        return self.scores

    #分かち書き
    def wakachi(self, doc):
        return self.tagger.parse(doc)
    
# WRDの検索
# 参考　論文の著者　https://speakerdeck.com/eumesy/optimal-transport-for-natural-language-processing
# コード　https://qiita.com/kenta1984/items/bad7e2f68331849d0053
class Word_Rotators:

    # 使用するモデル，MeCabのTagger，入力の分かち書き，
    def __init__(self, model, tagger, wkt, ids):
        self.model = model
        self.tagger = tagger
        self.w1 = load_pickle("./data/vec.binaryfile")
        self.m1 = load_pickle("./data/norm.binaryfile")
        self.wkt = wkt
        # self.ids = ids

    # 単語ベクトルの計算
    def get_w(self):
        w = [np.array(self.model.get_word_vector(' '.join(kw))) for kw in self.wkt]
        return w

    # ノルムの計算
    def get_z(self, w):
        z = 0
        for w_i in w:
            z += np.linalg.norm(w_i)
        return z

    # コストの計算
    def cos_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    # WRDで近いもの，遠いもの，無関係のものを計算
    def calc(self):
        result_c = []
        result_i = []
        for j, w1 in enumerate(self.w1):
            w2 = self.get_w()
            z2 = self.get_z(w2)
            m2 = [np.linalg.norm(w2_i) / z2 for w2_i in w2]
            c = []
            i = []
            for w1_i in w1:
                cos = [self.cos_sim(np.array(w1_i), np.array(w2_j)) for w2_j in w2]
                c.append([1 - sim for sim in cos])
                i.append([abs(sim) for sim in cos])
            result_c.append(round(ot.emd2(self.m1[j], m2, c), 6))
            result_i.append(round(ot.emd2(self.m1[j], m2, i), 6))
        return np.array(result_c), np.array(result_i)

# ファイル読み込みの関数
def load_pickle(path):
    with open(path, mode="rb") as f:
        data = pickle.load(f)
    return data

def load_json(path):
    with open(path, mode="r", encoding="utf8") as f:
        data = json.load(f)
    return data