#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

def get_summary(text,k):
	
    k = int(k)
    sentences = text.split(".")

    sentences = [j.strip() for j in sentences]
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
    sim_mat = np.zeros([len(sentences), len(sentences)])
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    for i in range(len(sentences)):
        
        for j in range(len(sentences)):
            
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    su = ""
    if k>len(text):
        for ki in range(len(text)):
            su += " " + ranked_sentences[ki][1]
     
    else:
        
        for ki in range(k):
            
            su += " " + ranked_sentences[ki][1]
    
    
    return su

if __name__ == "__main__":
	import sys
	print(get_summary(sys.argv[2],sys.argv[1]))
