from english_words import get_english_words_set
from collections import Counter
import random
import math

corpus = get_english_words_set(['web2'], lower=True)

def sequencer(s):
    seq = []

    for length in range(1, 4):  
        for i in range(len(s) - length + 1):
            seq.append(s[i:i + length])
    
    return seq

def sequence_all_words(corpus):
    corpus_sequence_mapping = {}

    for word in corpus:
        corpus_sequence_mapping[word] = sequencer(word)
    
    return corpus_sequence_mapping


def get_sequence_counts(sequences):

    cntr = Counter(
        seq for sequences in corpus_mapping.values() 
            for seq in sequences 
    )

    return cntr

def get_sequence_probas(sequence_counts):

    total_seqs = sum(sequence_counts.values())

    probas = {seq: counts /total_seqs for seq,counts in sequence_counts.items()}

    return probas

def sample_sequence(probas):
    sequences = list(probas.keys())
    weights = list(probas.values())
    return random.choices(sequences, weights=weights, k=1)[0]

def generate_word(probas, min_length=4, max_length=10):

    word = []
    
    while len(''.join(word)) < max_length:
        # Sample a random trigram
        ngram = sample_sequence(probas)
        if len(ngram) != 3:
            continue
        word.append(ngram)
        
        # Stop if we've reached a reasonable length
        if len(''.join(word)) >= min_length and random.random() < 0.35:
            break
    
    return word

def synthesize_words(probas,counts):
    #create 1K VALID words
    MAX_WORDS = 3000

    #key is new word, value is log_prob (log of product of ngrams)
    valid_words = {}
    
    while len(valid_words) < MAX_WORDS:
        print(len(valid_words))
        skip = False
        word_components = generate_word(probas)
        word = ''.join(word_components)
        prob = 1

        components = [s for s in sequencer(word) if len(s) ==3]

        for component in components:
            if len(component) == 3 and counts[component] == 1:
                skip = True

        for component in word_components:
            prob*=probas[component]

        if skip:
            continue

        valid_words[word] = math.log(prob)

    return valid_words



if __name__ == "__main__":

    corpus_mapping = sequence_all_words(corpus)

    sequence_counts = get_sequence_counts(corpus_mapping.values())

    sequence_distrubition = get_sequence_probas(sequence_counts)

    synthetic_words = synthesize_words(sequence_distrubition,sequence_counts)

    sorted_items = sorted(synthetic_words.items(), key=lambda item: item[1])
    print(sorted_items)



