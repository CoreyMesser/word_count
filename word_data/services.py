import re
from pyphen import Pyphen
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
                    pc.paragraph_length_by_sentence = len(self.paragraph_cleaner(chunk=chunk))
                    pc.paragraph_length_by_word = self.thing_counter(chunk=chunk)
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
        rs = re.split(r'[.?!]', chunk)
        for line in rs:
            if line == '\n':
                continue
            else:
                sl = Sentence()
                sl.sentence = line.lstrip()
                sl.paragraph_id = paragraph_id
                sl.sentence_length = self.thing_counter(chunk=line)
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
            sw.word_length = len(word)
            sw.syllables = self.syllable_counter(word=word)
            sw.sentence_id = sentence_id
            db.add(sw)
        db.commit()
        # query db for sentence lines
        # break apart words

    def dialogue_parser(self, chunk, paragraph_id):
        db = db_session()
        diag = re.search(r'\"', chunk).group()

        pass

    def white_space_stripper(self, strip):
        """General purpose white space stripper"""
        for string in strip:
            return string.lstrip()

    def comma_stripper(self, strip):
        """Strips commas from individual words"""
        comma = re.search(r',', strip)
        if comma:
            return strip.split(',')[0]
        else:
            return strip

    def syllable_counter(self, word, lang='en_US'):
        dic = Pyphen(lang=lang)
        hyphenated = dic.inserted(word=word)
        return hyphenated.count('-')+1

    def thing_counter(self, chunk):
        """len of a thing"""
        return len(chunk.split(' '))

    def paragraph_cleaner(self, chunk):
        """cleans out stupid /n"""
        c_split = re.split(r'[.?!]', chunk)
        for n in c_split:
            if n == '\n':
                c_split.pop(c_split.index(n))
        return c_split


class ReadingScores(object):

    def get_total_words(self, chunk):
        # SQL to grab total words from chunk?
        pass

    def average_sentence_len(self):
        pass

    def average_syllables_per_word(self):
        pass

    def flesch_reading_ease(self):
        avsl = self.average_sentence_len()
        aspw = self.average_syllables_per_word()
        return 206.853 - float(1.015 * avsl) - float(84.6 * aspw)

    def flesch_kincaid_grade(self):
        avsl = self.average_sentence_len()
        aspw = self.average_syllables_per_word()
        return float(0.39 * avsl) + float(11.8 * aspw) - 15.59


class DatabaseServices(object):

    def get_id(self, tab, col, string):
        db = db_session()
        row = db.query(tab).filter(col == string).first()
        return row.id

    """
    Populates empty columns
    """

    def paragraph_length_by_sentence(self):
        # establish db connection
        # loop or kwarg to fill paragraph.paragraph_length_by_sentence using
        # SQL:
        # select paragraph_id, count(sentence) from sentence group by sentence.paragraph_id
        pass

    def paragraph_length_by_word(self):
        # establish db connection
        # loop or kwarg to fill paragraph.paragraph_length_by_sentence using
        # SQL:
        # select paragraph.id as p_id, count(word) as w_count from words
        # join sentence on sentence.id = sentence_id
        # join paragraph on paragraph.id = sentence.paragraph_id
        # group by paragraph.id order by paragraph.id asc
        pass
