# vec2word
Semi-automated vocabulary generation from semantic vector models

This script generates a list of potential conlang word forms along with associated possible glosses based on a word-shape template and a word2vec-style semantic vector model. The process works something like this:

1. Acquire a word2vec-style semantic vector model (either word2vec binary format or text format).
2. Define a word-shape template.
3. Figure out how many word forms can be made from that template, and group vectors into that many clusters.
4. Use Principle Component Analysis to project the vector model down to the same number of dimensions as you have slots in your template.
5. Match the new model dimensions to slots based on how many phonemes can go in a slot vs. the variance in a given dimension (large phoneme range pairs with large variance), and then discretize those dimensions into the appropriate number of buckets.
5. Use the buckets each cluster-centroid vector ends up getting put in to select phonemes for each template slot and generate new conlang words, along with a list of all of the model words whose vectors ended up in that cluster.

This results in word forms in which each phoneme represents a category in some semantic classification scheme, rather like a traditional philosophical language--except, the categories are not always obviously-sensible, human-defined categories such as you might find in a thesaurus, but weird collections of whatever happens to project into similar places in low-dimensional space. Getting reasonable definitions for your new words will still require work at selecting among the various options provided to you, or making up a new one in a similar semantic space--whatever you decide that means. Ideally, this should result in a lexicon with lots of discoverable sound-symbolism, but very little obvious regular morphology. The various source words in each cluster are output in order of their distance from the most central prototype of the cluster--which usually means being ordered from most generic to most specific, but not always.

You could also decide that, rather than generating complete words, you just want to generate, e.g., individual syllables, which could then be compounded together to produce words with more specific meanings--essentially, simulating the process by which Chinese produced lots of homophones (single phonetic forms with wildly varying ambiguous meanings) and then used compounding to re-disambiguate the lexicon.

Or generate triliteral consonant roots, whose semantics will be narrowed down by intercalated vowel patterns.

Or something else entirely! Play around, experiment, have fun!

# Example use

`python vec2word.py model.bin "t,d,n,k,g,q,p,b,m" "i,u,e" "t,n,k,q,p,m" > syllables.txt`

This uses the `model.bin` model to produce "words" on a CVC template and save the results in `syllables.txt`. For longer templates, just add more command-line arguments, each consisting of a comma-separated list of phonemes/graphemes that are allowed in the slot.

Most models are really big, which means the clusters are *really big*, which can be overwhelming. So, if you put a number bigger than zero between the model file name and the first slot definition, it will output only that many of the most central members of each cluster.

Many pre-built word2vec models suitable for use with this script can be downloaded from the [NLPL Word Vectors Repository](http://vectors.nlpl.eu/repository/).
