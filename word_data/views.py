from word_data.services import WordCount

class Parse_File(object):
    wc = WordCount()

    def run_parse(self, file):
        self.wc.parse_file(file=file)

if __name__ == '__main__':
    file = '/home/pibblefiasco/Development/word_count/HRPG.txt'
    pf = Parse_File()
    pf.run_parse(file=file)