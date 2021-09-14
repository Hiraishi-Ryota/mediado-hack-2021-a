from gensim import models
from janome.tokenizer import Tokenizer
import numpy as np
import pickle

# これはサーバー実行時に起動する
try:
    model = models.Doc2Vec.load('doc2vec.model')
except:
    pass

tokenizer = Tokenizer()

vectors_path = "vectors.pkl"

def doc2vec(text):
    try:
        tokens = tokenizer.tokenize(text, wakati=True)
        vec = np.array(model.infer_vector(tokens))
    except:
        vec = np.random.rand(300)

    vec /= np.sqrt(np.dot(vec, vec))
    return vec

# 章のIDとテキストを入力すると，ベクトルを生成してvectors.pklに追記保存
def add_vector(id, doc):
    vectors = {
        "id2index": {},
        "index2id": [],
        "matrix": None
    }

    try:
        with open(vectors_path, "rb") as fp:
            vectors = pickle.load(fp)
    except:
        pass

    vector = doc2vec(doc)

    vectors["id2index"][id] = len(vectors["index2id"])
    vectors["index2id"].append(id)

    if vectors["matrix"] is None:
        vectors["matrix"] = vector.reshape(1, 300)
    else:
        vectors["matrix"] = np.append(vectors["matrix"], vector.reshape(1, 300), axis=0)

    with open(vectors_path, "wb") as fp:
        pickle.dump(vectors, fp)

# レコメンド
def search_vector(id, max):
    try:
        with open(vectors_path, "rb") as fp:
            vectors = pickle.load(fp)
    except:
        return []

    if id in vectors["id2index"]:
        index = vectors["id2index"][id]
        target_vector = vectors["matrix"][index]

        ranking = list(np.argsort(-np.dot(vectors["matrix"], target_vector)))
        ranking.remove(index)

        searched_ids = list(map(lambda index: vectors["index2id"][index], ranking[:max]))
        return searched_ids
    else:
        return []

if __name__ == "__main__":
    vec = doc2vec("テキスト（英語: text、ドイツ語: Text、フランス語: texte、テクスト）は、文章や文献のひとまとまりを指して呼ぶ呼称。 言葉によって編まれたもの、という含みを持つ語で、英語: textile（テキスタイル、「織物」）と同じくラテン語の「織る」が語源である。")
    print(vec)

    print("aというIDで追加")
    add_vector("11", "すもももももももものうち")

    print("bというIDで追加")
    add_vector("21", "ももくり3年かき8年")

    print("cというIDで追加")
    add_vector("31", "猿も木から落ちる")

    add_vector("41", "猿も木から落ちる")
    add_vector("51", "猿も木から落ちる")
    add_vector("61", "猿も木から落ちる")
    add_vector("71", "猿も木から落ちる")
    add_vector("81", "猿も木から落ちる")

    print("aというIDのドキュメントと似たドキュメントのIDを最大5件返します")
    print(search_vector("31", 5))
