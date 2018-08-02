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

    def run(self, file):
        print('Parsing File...')
        self.run_parse(file=file)
        print('Successfully Parsed File')
        print('Calculating Scores...')
        self.run_scores()
        print('Successfully Calculated Scores')

    def run_parse(self, file):
        self.wc.parse_file(file=file)

    def run_scores(self):
        self.rs.generate_sentence_scores(paragraph_id=1)


if __name__ == '__main__':
    # file = '/home/pibblefiasco/Development/word_count/writing_samples/HRPG.txt'
    file = '/home/pibblefiasco/Development/word_count/writing_samples/SpiceofLife_Short.txt'
    pf = Parse_File()
    pf.run(file=file)
    # pf = Parse_File()
    # pf.run_parse(file=file)
    # pf = Parse_File()
    # pf.run_scores()
