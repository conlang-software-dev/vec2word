import sys
import random
import numpy as np
from functools import reduce
from itertools import product
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import defaultdict

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
print(dims)
print(d_order)

model_file = sys.argv[1]
wv = KeyedVectors.load_word2vec_format(model_file, binary=(model_file.endswith('.bin')))

sample_count = K*50
vector_count = len(wv.vectors)
if sample_count > vector_count:
    sample_count = vector_count

print("Using", sample_count, "of", vector_count, "vectors for clustering")
samples = [wv.vectors[i,:] for i in select(sample_count, vector_count)]

km = KMeans(n_clusters=K)
km.fit(wv.vectors)
centers = km.cluster_centers_
print("Got Centers")

pca = PCA(n_components=D)
result = pca.fit_transform(centers)
r_order = np.lexsort((result[:,d_order]).T)
print("Sorted Centers")

labels2words = defaultdict(list)
if cluster_size == 0:
    labels = km.predict(wv.vectors)
    for i, l in enumerate(labels):
        labels2words[l].append(wv.index_to_key[i])
    print("Labelled all vectors")

print("Forms:", K)

for i, emes in enumerate(product(*segments)):
    center = centers[r_order[i],:]
    if cluster_size == 0:
        v1, v2 = wv.most_similar(positive=[center], topn=2)
        word = v1[0] if v1[0] is not None else v2[0]
        label = r_order[i]
        cluster = labels2words[label]
    else:
        cluster = [r[0] for r in wv.most_similar(positive=[center], topn=cluster_size)]
        word = cluster[0] if cluster[0] is not None else cluster[1]
    print(
        "".join(emes), ':',
        repr(word.encode("utf-8", errors='replace'))[2:-1] if word is not None else "?",
        len(cluster)
    )
    for w in sorted(w for w in cluster if w is not None and w != word):
        print('\t', repr(w.encode("utf-8", errors='replace'))[2:-1])
    print('==========')