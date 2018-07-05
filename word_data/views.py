from word_data.services import WordCount, DatabaseServices

class Parse_File(object):
    wc = WordCount()
    dbs = DatabaseServices()

    def run_parse(self, file):
        self.wc.parse_file(file=file)

    def run_query(self):
        self.dbs.get_sentence(paragraph_id=3)
        # self.dbs.get_syllable_total(sentence_id=3)


if __name__ == '__main__':
    file = '/home/pibblefiasco/Development/word_count/HRPG.txt'
    # pf = Parse_File()
    # pf.run_parse(file=file)
    pf = Parse_File()
    pf.run_query()
