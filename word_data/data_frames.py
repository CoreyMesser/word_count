import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns
sns.set_style(style='ticks')

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
        sentence = pd.read_sql_query('select sentence.id, count(words.sentence_id), sentence from words join sentence '
                                     'on sentence.id = sentence_id group by sentence.id order by sentence.id asc', en)
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

    def fre_graph_paragraph(self):
        y = pd.read_sql_query('SELECT flesch_reading_ease FROM paragraph order by paragraph.id asc ', en)
        x = pd.read_sql_query('SELECT id FROM paragraph order by paragraph.id asc', en)
        plt.plot(x, y)
        plt.xlabel('ID')
        plt.ylabel('Flesch Reading Ease')
        plt.title('Flesch Reading Ease Score')

        plt.show()

    def fre_graph_sentence(self):
        y = pd.read_sql_query('SELECT flesch_reading_ease FROM sentence order by sentence.id asc ', en)
        x = pd.read_sql_query('SELECT id FROM sentence order by sentence.id asc', en)
        u = pd.read_sql_query('SELECT flesch_kincaid_grade FROM sentence order by sentence.id asc ', en)
        v = pd.read_sql_query('SELECT id FROM sentence order by sentence.id asc', en)
        fig = plt.figure()
        axes = fig.add_axes([0.1,0.1,0.8,0.8])

        axes.plot(x, y, 'b', label="FRE")
        axes.plot(x, u, 'r', label="FKG")
        axes.set_xlabel('ID')
        axes.set_ylabel('Flesch Reading Ease')
        axes.set_title('Flesch Reading Ease Score')
        axes.legend()

        plt.show()

    def seaborn_jointplot_fre(self):
        sentence = pd.read_sql_query('SELECT * FROM paragraph', en)
        # x = pd.read_sql_query('SELECT id FROM sentence order by sentence.id asc', en)
        sns.jointplot(x='flesch_kincaid_grade', y='flesch_reading_ease', data=sentence, kind='hex', stat_func=kendalltau, color="#4CB391")
        plt.show()


if __name__ == '__main__':
    rep = Reports()
    rep.seaborn_jointplot_fre()

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
