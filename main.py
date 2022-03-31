from lib import dictionary, wallpaper, wordlist

RUN_LIMIT = 900

def main():
    for i in range(RUN_LIMIT):
        print(f'Starting iteration {i}..')

        # get a word from pending words list
        word = wordlist.get_pending_word()
        print(f'Got word: {word}')
        if word == None:
            print('No more words to process')
            break

        # get spanish-english dictionary entry for word
        entry = dictionary.get_entry(word)
        print(f'Got definition: {entry}')
        if entry == None:
            print('No definition found for word')
        else:
            # write text to a jpg file that can be used as wallpaper
            wallpaper.create_text_wallpaper(entry)
            print(f'Created wallpaper for word: {word}')

        # remove word from pending words list
        print(f'Marking {word} as processed..')
        wordlist.mark_word_processed(word)

        print(f'Finished iteration {i}')

if __name__ == '__main__':
    main()