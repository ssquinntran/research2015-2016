import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_lang_vec(filename, lv, cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = random_idx.generate_RI_text_fast(N, lv, cz, ordered, filename, alphabet)#"preprocessed_texts/AliceInWonderland.txt", alph)
        total_lang += lang_vector
    return total_lang

# 1 indexed
def initialize(cluster_sizes):
    #for each n, dictionary of key: n gram and value: frequency
    n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]
    # save vectors to file
    fwrite = open("intermediate/n_gram_frequencies", "w")
    pickle.dump(n_gram_frequencies, fwrite)
    fwrite.close()
    return n_gram_frequencies

def initialize_from_file():
    fread = open("intermediate/n_gram_frequencies", "r")
    n_gram_frequencies = pickle.load(fread)
    fread.close()
    return n_gram_frequencies

def write_data_structures(data_structures=[], file_paths=[]):
    for i in range(0,len(file_paths)):
        fwrite = open(file_paths[i], "w")
        pickle.dump(data_structures[i], fwrite)
        fwrite.close()

def get_letter_vec(s, letter_vec):
    if(len(s) == 1):
        return letter_vec[alphabet.index(s)];
    vec = letter_vec[alphabet.index(s[0])];
    for i in s[1:]:
        vec = np.multiply(np.roll(vec, 1), letter_vec[alphabet.index(i)]);
    return vec;

def recover_frequency(letter_vec, s, array):
    vec = get_letter_vec(s, letter_vec);
    return np.dot(vec, array[len(s)-1]);
#should we separate by cluster sizes? following precedent, guess not
def vocab_vector(lv, filepath="preprocessed_texts/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read()
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    vocab_vec = np.zeros((1,N))
    max_length = 0
    for word in text:
        #print "generating vocab vector of cluster size", len(word)
        word_vec = random_idx.id_vector(N, word, alphabet, lv, ordered)
        vocab_vec += word_vec
        if len(word) > max_length:
            max_length = len(word)
    f.close()
    return vocab_vec, max_length
#array with cluster size as index, the dictionary of words in that index
#http://www.nltk.org/howto/probability.html
def vocab(max_word_length, filepath="preprocessed_texts/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read();
    text = text.split(" ")
    # verb_fd = nltk.FreqDist(word for (word, tag) in verb_tagged)
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    #max word length is 20 letters lol
    array = [{} for i in range(0,max_word_length)]

    for word in text:
        if word not in array[len(word)-1].keys():
            array[len(word)-1][word] = 1
        else:
            array[len(word)-1][word] += 1
    f.close()
    return array
