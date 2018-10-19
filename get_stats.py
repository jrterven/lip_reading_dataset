import glob
import os
from collections import Counter

results_dir = '/datasets/Our_dataset/results'

# load all the .txt files recursively
all_annotations = glob.glob(results_dir + '/**/*.txt', recursive=True)
print(len(all_annotations), 'files')

# count all the words
wordcount = Counter({})
for ann_file in all_annotations:
    file = open(ann_file, "r")
    counts = Counter(file.read().split())
    wordcount += counts
    file.close()

print(wordcount)
#print(list(wordcount))

