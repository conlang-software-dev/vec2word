import sys
import numpy as np
from gensim.models import KeyedVectors

# Rotate v in the plane of x and y through the angle between x and y
def rot_plane(v, x, y):
  vx = np.dot(v, x)
  vy = np.dot(v, y)
  xcomp = -vx - vy
  ycomp = vx - vy
  return v + x * xcomp + y * ycomp

def s(w):
    return "None" if w is None else repr(w.encode("utf-8", errors='replace'))[2:-1]

def diffs(keys):
    # Maybe this could be replaced with just a random vector generator?
    # But then why does the rotation matter? I dunno!
    for i, w1 in enumerate(keys):
        if w1 is None: continue
        v = wv.vectors[i]
        for j in range(i+1, len(keys)):
            w2 = keys[j]
            if w2 is None: continue
            yield (i, j, v, wv.vectors[j])

def test_relation(i, j, v1, v2):
    d = v2 - v1
    n = np.linalg.norm(d)
    print("d", n)
    print("d", n, file=sys.stderr)
    if n > 1.1: return # this may be a model-specific parameter
    for k, w1 in enumerate(keys):
        if w1 is None or k == i or k == j: continue
        v3 = wv.vectors[k]
        r = rot_plane(d, v1, v3)
        (w2, e) = wv.similar_by_vector(v3 + r, topn=1)[0]
        # This e > 0.75 check feels backwards, but it seems to be critical
        # Why does filtering out results that are "too good" actually make the results better?
        # I haven't a single clue!
        if w2 is None or e > 0.75 or w2 == w1: continue
        (w3, _) = wv.similar_by_vector(wv[w2] - r, topn=1)[0]
        if w3 == w1: yield (w1,w2,e)

model_file = sys.argv[1]
wv = KeyedVectors.load_word2vec_format(model_file, binary=(model_file.endswith('.bin')))

keys = wv.index_to_key

# just testing diffs between unique pairs, ignoring sign
count = float(len(keys) * (len(keys) - 1) / 2)

for p, (i, j, v1, v2) in enumerate(diffs(keys)):
    print(p, round(100 * p / count), "%", file=sys.stderr)
    
    s1 = s(keys[i])
    s2 = s(keys[j])
    print(s2, ">", s1, file=sys.stderr)
    
    rel = list(test_relation(i, j, v2, v1))
    if len(rel) > 0:
        print(s2, ">", s1)
        for w1,w2,d in rel:
            s1 = s(w1)
            s2 = s(w2)
            print(s1, s2, d)
            print(s1, s2, d, file=sys.stderr)