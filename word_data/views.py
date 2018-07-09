import logging
from word_data.services import WordCount, DatabaseServices, ReadingScores

logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
handler = logging.FileHandler('/home/pibblefiasco/Development/word_count/word_data/logs/pool_logs.log')
handler.setLevel(logging.INFO)

class Parse_File(object):
    wc = WordCount()
    dbs = DatabaseServices()
    rs = ReadingScores()

    def run_parse(self, file):
        self.wc.parse_file(file=file)

    def run_query(self):
        self.dbs.get_sentence(paragraph_id=3)
        # self.dbs.get_syllable_total(sentence_id=3)

    def run_scores(self):
        self.rs.generate_sentence_scores(paragraph_id=3)


if __name__ == '__main__':
    file = '/home/pibblefiasco/Development/word_count/HRPG.txt'
    # pf = Parse_File()
    # pf.run_parse(file=file)
    pf = Parse_File()
    pf.run_scores()
