import re
import math
from pyphen import Pyphen
from sqlalchemy import update
from word_data.database import db_session
from word_data.models import Dialogue, Paragraph, Sentence, Words, ParagraphTemplate

class Session(object):
    def startSession(self):
        session = []
        return session

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
            chunk_id, sent_id = 1, 1
            for chunk in raw_file:
                if len(chunk) > 1:
                    pc = Paragraph()
                    pc.paragraph = chunk
                    pc.paragraph_length_by_sentence = len(self.paragraph_cleaner(chunk=chunk))
                    pc.paragraph_length_by_word = self.thing_counter(chunk=chunk)
                    db.add(pc)
                    db.commit()
                    sent_id = self.parse_sentence(chunk=chunk, paragraph_id=chunk_id, sentence_id=sent_id)
                    chunk_id += 1

    def parse_file(self, file):
        self.open_file(file=file)

    def parse_sentence(self, chunk, paragraph_id, sentence_id):
        """
        Takes a paragraph chunk and splits it up into sentences by punctuation
        :param chunk:
        :param paragraph_id:
        :param sentence_id:
        :return:
        """
        db = db_session()
        rs = re.split(r'[.?!"“”]', chunk)
        for line in rs:
            line = line.lstrip()
            if line == '\n' or line == ' \n' or line == '"' or line == '“' or line == '”' or line == ' ' or len(line) < 1:
                continue
            else:
                sl = Sentence()
                sl.sentence = line.lstrip()
                sl.paragraph_id = paragraph_id
                sl.sentence_length = self.thing_counter(chunk=line.lstrip())
                db.add(sl)
                self.parse_word(line=line.lstrip(), sentence_id=sentence_id)
                db.commit()
                sentence_id += 1
        return sentence_id

    def parse_word(self, line, sentence_id):
        """
        Takes a sentence line and splits it up into words by white space
        :param line:
        :param sentence_id:
        :return:
        """
        db = db_session()
        ws = line.split(' ')

        tot_syll = 0
        rhythm_by_syll = []
        rhythm_by_word = []

        for word in ws:
            word = self.comma_stripper(strip=word)
            sw = Words()
            sw.word = word
            word_len = len(word)
            sw.word_length = word_len
            rhythm_by_word.append(word_len)
            syllables = self.syllable_counter(word=word)
            sw.syllables = syllables
            rhythm_by_syll.append(syllables)
            sw.sentence_id = sentence_id
            db.add(sw)

        # tot_syll = sum(rhythm_by_syll)
        # sl = Sentence()
        # sl.total_syllables = tot_syll
        # sl.rhythm_by_syllable = rhythm_by_syll
        # sl.rhythm_by_word_len = rhythm_by_word
        # db.add(sl)
        db.commit()

    def comma_stripper(self, strip):
        """Strips commas from individual words"""
        comma = re.search(r',', strip)
        if comma:
            return strip.split(',')[0]
        else:
            return strip

    def syllable_counter(self, word, lang='en_US'):
        """uses the Pyphen library to hyphenate the word and then
        count the hyphens +1 to simulate syllables in english"""
        dic = Pyphen(lang=lang)
        hyphenated = dic.inserted(word=word)
        return hyphenated.count('-')+1

    def thing_counter(self, chunk):
        """len of a thing"""
        thing = len(chunk.lstrip().split(' '))
        return thing

    def paragraph_cleaner(self, chunk):
        """cleans out stupid \n so I can get on with my life and not waste an hour trying to do it with one line"""
        c_split = re.split(r'[.?!]', chunk)
        for n in c_split:
            if n == '\n' or n == ' \n':
                c_split.pop(c_split.index(n))
        return c_split


class ReadingScores(object):

    def get_session(self, default_id):
        db_services = DatabaseServices()
        return db_services.get_sentence(paragraph_id=default_id)

    def get_total_words(self, session):
        return session.sentence_length

    def get_total_syllables(self, session):
        db_services = DatabaseServices()
        return db_services.get_syllable_total(session=session)

    def average_sentence_len(self, session):
        total_words = self.get_total_words(session=session)
        total_sentences = 1
        if total_words == 0:
            return 0
        else:
            return total_words/total_sentences

    def average_syllables_per_word(self, session):
        total_syllables = self.get_total_syllables(session=session)
        total_words = self.get_total_words(session=session)
        if total_words == 0:
            return 0
        else:
            return total_syllables/total_words

    def flesch_reading_ease(self, session):
        avsl = self.average_sentence_len(session=session)
        aspw = self.average_syllables_per_word(session=session)
        return 206.853 - float(1.015 * avsl) - float(84.6 * aspw)

    def flesch_kincaid_grade(self, session):
        avsl = self.average_sentence_len(session=session)
        aspw = self.average_syllables_per_word(session=session)
        return float(0.39 * avsl) + float(11.8 * aspw) - 15.59

    def generate_sentence_scores(self, paragraph_id=1):
        db = db_session()
        dbs = DatabaseServices()
        rows = db.query(Paragraph).count()

        while paragraph_id <= rows:
            para_template = ParagraphTemplate()
            session = self.get_session(default_id=paragraph_id)

            for entry in session:
                fre = math.floor(self.flesch_reading_ease(session=entry)*100)/100
                fkg = math.floor(self.flesch_kincaid_grade(session=entry)*100)/100

                db.query(Sentence).filter(Sentence.id == entry.id).update(values={'flesch_reading_ease': fre})
                db.query(Sentence).filter(Sentence.id == entry.id).update(values={'flesch_kincaid_grade': fkg})
                db.commit()

                para_template.fre += fre
                para_template.fkg += fkg

            paragraph_len_by_sent = dbs.get_paragraph_length_by_sentence(paragraph_id=paragraph_id)
            paragraph_fre = para_template.fre / paragraph_len_by_sent
            paragraph_fkg = para_template.fkg / paragraph_len_by_sent

            db.query(Paragraph).filter(Paragraph.id == paragraph_id).update(
                values={'flesch_reading_ease': paragraph_fre})
            db.query(Paragraph).filter(Paragraph.id == paragraph_id).update(
                values={'flesch_kincaid_grade': paragraph_fkg})
            db.commit()
            paragraph_id += 1


class DatabaseServices(object):

    def get_id(self, tab, col, string):
        db = db_session()
        row = db.query(tab).filter(col == string).first()
        return row.id

    def get_sentence(self, paragraph_id):
        db = db_session()
        return db.query(Sentence).filter(Sentence.paragraph_id == paragraph_id).all()

    def get_syllable_total(self, session):
        a = 0
        db = db_session()
        sess = db.query(Words).filter(Words.sentence_id == session.id).all()
        for _row in sess:
            a = _row.syllables + a
        return a

    def get_paragraph_length_by_sentence(self, paragraph_id):
        db = db_session()
        sess = db.query(Paragraph).filter(Paragraph.id == paragraph_id).first()
        return sess.paragraph_length_by_sentence
