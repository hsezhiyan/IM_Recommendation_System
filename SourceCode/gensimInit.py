import numpy
import gensim.downloader as api

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec

# path = get_tmpfile("word2vec.model")
# #corpus = api.load("wiki-english-20171001")
# corpus = api.load("text8")
# model = Word2Vec(corpus, size=100, window=5, min_count=1, workers=4)
# model.save("word2vec.model")
model = Word2Vec.load("word2vec.model")

vector = model.wv['java'] 
vector2 = model.wv['python'] 
vector3 = model.wv['english'] 

print(numpy.linalg.norm(vector-vector2))
print(numpy.linalg.norm(vector-vector3))
