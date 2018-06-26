import re
from word_data.database import db_session
from word_data.models import Dialogue, Paragraph, Sentence, Words


class WordCount(object):

    def __init__(self):
        self.db_service = DatabaseServices()

    def open_file(self, file):
        """
        Opens file and parses it into chunks which is then written to the data base
        :param file:
        :return:
        """
        with open(file=file, encoding='utf=8') as raw_file:
            db = db_session()
            for chunk in raw_file:
                if len(chunk) > 1:
                    pc = Paragraph()
                    pc.paragraph = chunk
                    db.add(pc)
                    db.commit()
                    paragraph_id = self.db_service.get_id(tab=Paragraph, col=Paragraph.paragraph, string=chunk)
                    self.parse_sentence(chunk=chunk, paragraph_id=paragraph_id)

    def parse_file(self, file):
        self.open_file(file=file)

    def parse_sentence(self, chunk, paragraph_id):
        """
        Takes a paragraph chunk and splits it up into sentences by punctuation
        :param chunk:
        :param paragraph_id:
        :return:
        """
        db = db_session()
        rs = re.split('[.?!]', chunk)
        for line in rs:
            if line == '\n':
                continue
            else:
                sl = Sentence()
                sl.sentence = line.lstrip()
                sl.paragraph_id = paragraph_id
                db.add(sl)
                db.commit()
                sentence_id = self.db_service.get_id(tab=Sentence, col=Sentence.sentence, string=line.lstrip())
                self.parse_word(line=line.lstrip(), sentence_id=sentence_id)

    def parse_word(self, line, sentence_id):
        """
        Takes a sentence line and splits it up into words by white space
        :param line:
        :param sentence_id:
        :return:
        """
        db = db_session()
        ws = line.split(' ')
        for word in ws:
            word = self.comma_stripper(strip=word)
            sw = Words()
            sw.word = word
            sw.sentence_id = sentence_id
            db.add(sw)
        db.commit()
        # query db for sentence lines
        # break apart words

    def dialogue_parser(self, chunk, paragraph_id):
        db = db_session()
        diag = re.search(r'\"', chunk).group()

        pass

    def stripper(self, strip):
        """General service white space stripper"""
        for string in strip:
            return string.lstrip()

    def comma_stripper(self, strip):
        """Strips commas from individual words"""
        comma = re.search(r',', strip)
        if comma:
            return strip.split(',')[0]
        else:
            return strip


class DatabaseServices(object):

    def get_id(self, tab, col, string):
        db = db_session()
        row = db.query(tab).filter(col == string).first()
        return row.id
