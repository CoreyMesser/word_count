import os
import sqlalchemy
import re
from word_data.database import db_session
from word_data.models import Dialogue, Paragraph, Sentence, Word


class WordCount(object):

    def __init__(self):
        self.db_service = DatabaseServices()

    def open_file(self, file):
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
        raw_file = self.open_file(file=file)
        # self.parse_paragraph(file=raw_file)
        # parse_sentence
        # parse_word
        pass

    def parse_paragraph(self, file):

        # not really paragraphs, chunks
        # break apart file by page breaks
        # single sentence "paragraphs" are fine, this is a top level id
        # validate a paragraph is composed of more than one sentence
        # write to db
        pass

    def parse_sentence(self, chunk, paragraph_id):
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

        # query db for paragraph chunk
        # break apart paragraph by punctuation
        # dialogue parser - speaker should be included

        # regex?
        # write to db
        pass

    def parse_word(self, line, sentence_id):
        db = db_session()
        ws = line.split(' ')
        for word in ws:
            sw = Word()
            sw.word = word
            sw.sentence_id = sentence_id
            db.add(sw)
        db.commit()
        # query db for sentence lines
        # break apart words


    def dialogue_parser(self, query):
        # if
        pass

    def stripper(self, strip):
        for string in strip:
            strip_string = string.lstrip()
            return strip_string


class DatabaseServices(object):

    def get_id(self, tab, col, string):
        db = db_session()
        row = db.query(tab).filter(col == string).first()
        return row.id

    # def word_dict(self):
    #     db = get_db()
    #     line_n = 0
    #     words_l = []
    #     words_s = [] #split words
    #     words_d = {} #display words
    #
    #     #open file
    #     with open('/Users/cmesser/Development/word_data/HRPG.txt', encoding='utf-8') as word_list:
    #         #split lines
    #         for a_line in word_list:
    #             line_n += 1
    #             line_s = words_l.append(a_line.rstrip())
    #             #  split words
    #             for a_word in a_line.split(' '):
    #                 words_s.append(a_word)

    #  isolate words
    # for w_word in words_s:
    #     if w_word not in words_d.keys():
    #         word_data = words_s.count(w_word)
    #         words_d.update({w_word: word_data})
    #     else:
    #         continue

# count as a function
