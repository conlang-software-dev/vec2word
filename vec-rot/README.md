# Discover fuzzy relations... of some sort

`python vec-rot.py {model file} > output.txt`

The program expects output to redirected to a file, and prints diagnostic info to stderr.

This is an accidental side-product of trying to automatically extract analogy sets. It completely fails at that, but the first time I tested this general approach (get a random difference vector, try to apply it to a new base after rotating it from its original position to the new base position, and then see if wherever it takes you lets you get back again; the idea here was to try to come up with some way of judging if a relationship is "real" other than having an arbitrary similarity cut-off), it seemed to spit out hyponym sets. In fact, it's a lot messier than that--it seems to extract sets of words that all have a similar relationship *of some sort* with a common target word, of which hypoynmy is one possibility, and I am not sure exactly what it is doing. I thought I had it figured out, until I realized that I had a less-than sign accidentally exchanged for a less-than sign... and "fixing" that ended up producing garbage!

So, I have tried to make it do whatever it is that it does reasonably quickly, and cleaned it up for other people to look at. Maybe it will be useful, or at least interpretable, to someone else.
