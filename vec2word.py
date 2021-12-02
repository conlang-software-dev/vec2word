import sys
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from collections import defaultdict

segments = [a.split(',') for a in sys.argv[2:]]
dims = [len(a) for a in segments]
D = len(dims)

s_order = sorted(range(D), key=lambda n: dims[n])
slot_sizes = [0]*D
for k, s in enumerate(s_order):
	slot_sizes[s] = k

model_file = sys.argv[1]
wv = KeyedVectors.load_word2vec_format(model_file, binary=(model_file.endswith('.bin')))
pca = PCA(n_components=D)
result = pca.fit_transform(wv.vectors)

# indexes of feature columns from smallest variance to largest
# c_order[slot_sizes[slot]] gives the index of the column to
# reference for a given output slot.
c_order = list(range(D))
c_order.reverse()

buckets = []
for slot in range(D):
	size = slot_sizes[slot]
	c = c_order[slot_sizes[slot]]
	col = result[:,c]

	# how should we bucket that column's values?
	divisions = dims[slot]
	l = len(col) - 1
	vals = sorted(col)
	buckets.append([vals[round((i+1)*l/divisions)] for i in range(divisions)])

groups = defaultdict(list)

for word, i in wv.key_to_index.items():
	features = result[i,:] # get row
	form = ""
	for slot, slot_segments in enumerate(segments):
		c = c_order[slot_sizes[slot]]
		f = features[c] # get column
		b = buckets[slot]
		# determine what bucket this value falls in
		k = 0
		while f > b[k]:
			k += 1
		form += slot_segments[k]
	groups[form].append(word)

print("Forms:", len(groups))

for k, v in groups.items():
	print(k, len(v))
	for word in sorted(v):
		try:
			print('\t', word)
		except:
			pass
	print('==========')
