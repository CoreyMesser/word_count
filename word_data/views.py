import logging
from word_data.services import WordCount, DatabaseServices, ReadingScores
from word_data.decorators import time_tracker

logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
handler = logging.FileHandler('/home/pibblefiasco/Development/word_count/word_data/logs/pool_logs.log')
handler.setLevel(logging.INFO)


def _log(message):
    print('[SimpleTimeTracker] {function_name} {total_time:.3f}'.format(**message))


class Parse_File(object):
    wc = WordCount()
    dbs = DatabaseServices()
    rs = ReadingScores()

    def run(self, path, file):
        print('Parsing File...')
        self.run_parse(path=path, file=file)
        print('Successfully Parsed File')
        print('Calculating Scores...')
        self.run_scores()
        print('Successfully Calculated Scores')

    @time_tracker(_log)
    def run_parse(self, path, file):
        self.wc.parse_file(path=path, file=file)

    @time_tracker(_log)
    def run_scores(self):
        self.rs.generate_sentence_scores(paragraph_id=1)


if __name__ == '__main__':
    path = '/home/pibblefiasco/Development/word_count/writing_samples/'
    filename = 'muchado_a2s1.txt'
    pf = Parse_File()
    pf.run(path=path, file=filename)
    # pf = Parse_File()
    # pf.run_parse(file=file)
    # pf = Parse_File()
    # pf.run_scores()
