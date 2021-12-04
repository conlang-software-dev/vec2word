import sys
import random
import operator
import numpy as np
from functools import reduce
from itertools import product
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def select(k, n):
    value = list(range(k))
    rest = dict()
    for i in range(k):
        j = random.randrange(i, n)
        if j < k:
            # Both elements to be swapped are in the selection
            value[i], value[j] = value[j], value[i]
        elif j in rest:
            # Element j has been swapped before
            value[i], rest[j] = rest[j], value[i]
        else:
            # The value at j is still j, we now add it to the virtual array
            rest[j] = value[i]
            value[i] = j
    return value

cluster_size = 0
try:
    cluster_size = int(sys.argv[2])
except:
    pass

segments = [a.split(',') for a in sys.argv[(2 if cluster_size == 0 else 3):]]
dims = [len(a) for a in segments]
D = len(dims)
K = reduce(lambda a,b: a*b, dims)

d_order = np.lexsort((dims,))

model_file = sys.argv[1]
wv = KeyedVectors.load_word2vec_format(model_file, binary=(model_file.endswith('.bin')))

sample_count = K*50
vector_count = len(wv.vectors)
if sample_count > vector_count:
    sample_count = vector_count

print("Used", sample_count, "of", vector_count, "vectors for clustering")
samples = [wv.vectors[i,:] for i in select(sample_count, vector_count)]

km = KMeans(n_clusters=K)

if cluster_size == 0:
    labels2words = [list() for _ in range(K)]
    labels = km.fit_predict(wv.vectors)
    centers = km.cluster_centers_
    for i, l in enumerate(labels):
        w = wv.index_to_key[i]
        if w is not None:
            labels2words[l].append(w)
else:
    labels2words = []
    km.fit(wv.vectors)
    centers = km.cluster_centers_
    for center in centers:
        cluster = [r[0] for r in wv.most_similar(positive=[center], topn=(cluster_size+1)) if r[0] is not None]
        if len(cluster) > cluster_size: cluster.pop()
        labels2words.append(cluster)

pca = PCA(n_components=D)
result = pca.fit_transform(centers)
r_order = np.lexsort((result[:,d_order]).T)

print("Forms:", K)

for i, emes in enumerate(product(*segments)):
    center = centers[r_order[i],:]
    cluster = labels2words[r_order[i]]
    if cluster_size == 0:
        distances = wv.distances(center, cluster)
        cluster = [k for k, _ in sorted(zip(cluster, distances), key=operator.itemgetter(1))]

    word = cluster[0]
    print(
        "".join(emes), ':',
        repr(word.encode("utf-8", errors='replace'))[2:-1],
        len(cluster)
    )
    for w in cluster[1:]:
        print('\t', repr(w.encode("utf-8", errors='replace'))[2:-1])
    print('==========')