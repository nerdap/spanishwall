
import os
WORDS_FILE = os.path.realpath('assets/words.txt')
PROCESSED_FILE = os.path.realpath('assets/processed.txt')

def _read_wordlist(filename):
    wordlist = []
    with open(filename) as file:
        return set([
            line.strip()
            for line in file.readlines()
        ])

def get_pending_word():
    all_words = _read_wordlist(WORDS_FILE)
    processed_words = _read_wordlist(PROCESSED_FILE)
    unused_words = [
        word
        for word in all_words
        if word not in processed_words
    ]
    if len(unused_words) == 0:
        return None
    return unused_words[0]

def mark_word_processed(word):
    with open(PROCESSED_FILE, 'a') as file:
        file.write(word + '\n')