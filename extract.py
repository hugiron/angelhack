import gensim
from pymystem3 import Mystem

word2vec = gensim.models.Word2Vec.load('word2vec_model')
wv = word2vec.wv
del word2vec

tfidf = gensim.models.TfidfModel.load('tfidf_model')
dictionary = gensim.corpora.Dictionary.load('dictionary')
mystem = Mystem()


def extract_lemms(doc):
    return list(filter(lambda x: x[0].isalpha(), mystem.lemmatize(doc)))


def extract_from_doc(doc, top=5):
    lemms = extract_lemms(doc)
    doc_bow = dictionary.doc2bow(lemms)
    tmp = tfidf[doc_bow]

    res = map(lambda x: (dictionary.get(x[0]), x[1]), tmp)

    res = filter(lambda x: ord('а') <= ord(x[0][0]) <= ord('я'), res)

    return sorted(res, key=lambda x: x[1])[-top:]


def extract_from_docs(docs, top=5):
    tmp = map(lambda x: extract_from_doc(x, top), docs)
    res = []

    for keywords in tmp:
        for keyword in keywords:
            word = keyword[0]
            k = keyword[1]

            res.append((word, k))

    uniq = set()
    output = []

    for x in res:
        if x[0] not in uniq:
            uniq.add(x[0])
            output.append(x)

    output = filter(lambda x: ord('а') <= ord(x[0][0]) <= ord('я'), output)

    return sorted(output, key=lambda x: x[1])[-top:]
