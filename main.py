from english_words import get_english_words_set
from collections import Counter

corpus = get_english_words_set(['web2'], lower=True)

def sequencer(s):
    seq = []

    for length in range(1, 4):  # 1, 2, 3
        for i in range(len(s) - length + 1):
            seq.append(s[i:i + length])
    
    return seq

def sequence_all_words(corpus):
    corpus_sequence_mapping = {}

    for word in corpus:
        corpus_sequence_mapping[word] = sequencer(word)
    
    return corpus_sequence_mapping


def remove_unique_words(corpus_mapping):
    #removes words from corpus if any trigram is unique to only them

    trigram_counts = Counter(
        seq for sequences in corpus_mapping.values() 
            for seq in sequences if len(seq) == 3
    )

    filtered_words = {
        word:seqs for word,seqs in corpus_mapping.items()
        if all(trigram_counts[seq]>1 for seq in seqs if len(seq)==3)
    }

    return filtered_words


if __name__ == "__main__":

    corpus_mapping = sequence_all_words(corpus)

