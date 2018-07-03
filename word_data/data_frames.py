import pandas as pd
import numpy as np

from word_data.database import engine as en
from word_data.constants import SystemConstants


class Reports(object):

    def __init__(self):
        self.csv_loc = SystemConstants().CSV_LOCATION
        self.csv_ext = SystemConstants().CSV_EXTENTION

    def file_name_and_location(self):
        file_name = input(SystemConstants().FILE_NAME_DIALOGUE)
        return self.csv_loc + file_name + self.csv_ext

    def create_data_frame(self, query):
        df = pd.DataFrame(query)
        name_and_loc = self.file_name_and_location()
        df.to_csv(name_and_loc)

    def word_totals_csv(self):
        words = pd.read_sql_query('SELECT word, COUNT(1) FROM words GROUP BY word', en)
        self.create_data_frame(query=words)

    def sentence_length(self):
        sentence = pd.read_sql_query('select sentence.id, count(words.sentence_id), sentence from words join sentence on sentence.id = sentence_id group by sentence.id order by sentence.id asc', en)
        # sentence_words = pd.read_sql_query('SELECT LENGTH(sentence), sentence FROM sentence INNER JOIN words on words.id = sentence.id', en)
        self.create_data_frame(query=sentence)

    def word_length(self):
        word_len = pd.read_sql_query('select sentence_id, length(words.word) as word_len, word from words', en)
        self.create_data_frame(query=word_len)

    def average_complexity_score(self):
        complexity_score = pd.read_sql_query('', en)
        # calculate word len
        # calculate sentence len
        # add up word total for sentence / by sentence len

if __name__ == '__main__':
    rep = Reports()
    rep.word_length()

# sentence length
# average sentence length
# largest average word in sentence
#
# sentence patterns
# word patterns in sentence
# beats
# number of similar/same words in a sentence
# complexity of word/ length
#
# syllyables per word, per sentence
# iambic pentameter
