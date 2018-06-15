import os
import sqlite3


def word_dict():
    db = get_db()
    line_n = 0
    words_l = []
    words_s = [] #split words
    words_d = {} #display words

    #open file
    with open('/Users/cmesser/Development/word_count/HRPG.txt', encoding='utf-8') as word_list:
        #split lines
        for a_line in word_list:
            line_n += 1
            line_s = words_l.append(a_line.rstrip())
            #  split words
            for a_word in a_line.split(' '):
                words_s.append(a_word)

        #  isolate words
        for w_word in words_s:
            if w_word not in words_d.keys():
                word_count = words_s.count(w_word)
                words_d.update({w_word: word_count})
            else:
                continue

    return render_template("index.html", words_d=words_d)