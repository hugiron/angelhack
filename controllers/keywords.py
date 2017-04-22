import gensim
from pymystem3 import Mystem

word2vec = gensim.models.Word2Vec.load('word2vec_model')
wv = word2vec.wv
del word2vec

tfidf = gensim.models.TfidfModel.load('tfidf_model')
dictionary = gensim.corpora.Dictionary.load('dictionary')
mystem = Mystem()


def extract_from_doc(doc, top=5):
    lemms = list(filter(lambda x: x[0].isalpha(), mystem.lemmatize(doc)))
    doc_bow = dictionary.doc2bow(lemms)
    res = tfidf[doc_bow]

    return sorted(res, key=lambda x: x[1])[-top:]


def extrac_from_docs(docs, top=5):
    keywords = map(extract_from_doc, docs)
    res = []

    for keyword in keywords:
        word = dictionary.get(keyword[0])
        k = keyword[1]

        res.append((word, k))

        for x in wv.most_similar_cosmul(word):
            new_word = x[0]
            k1 = x[1]

            res.append((new_word, k * k1))

    return sorted(res, key=lambda x: x[1])[-top:]
