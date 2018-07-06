from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Paragraph(Base):
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True, server_default=text("nextval('paragraph_id_seq'::regclass)"))
    paragraph = Column(Text)
    paragraph_length_by_sentence = Column(Integer)
    paragraph_length_by_word = Column(Integer)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, server_default=text("nextval('words_id_seq'::regclass)"))
    sentence_id = Column(Integer, nullable=False)
    word = Column(Text, nullable=False)
    word_length = Column(Integer, nullable=False)
    syllables = Column(Integer, nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Sentence(Base):
    __tablename__ = 'sentence'

    id = Column(Integer, primary_key=True, server_default=text("nextval('sentence_id_seq'::regclass)"))
    paragraph_id = Column(ForeignKey('paragraph.id'), nullable=False)
    sentence = Column(Text, nullable=False)
    sentence_length = Column(Integer, nullable=False)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))

    paragraph = relationship('Paragraph')


class Dialogue(Base):
    __tablename__ = 'dialogue'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dialogue_id_seq'::regclass)"))
    paragraph_id = Column(ForeignKey('paragraph.id'), nullable=False)
    dialogue = Column(Text, nullable=False)
    dialogue_length = Column(Integer, nullable=False)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    sentence_ids = Column(ForeignKey('sentence.id'), nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))

    paragraph = relationship('Paragraph')
    sentence = relationship('Sentence')



class ParagraphTemplate(object):
    def __init__(self):
        self.id = 0
        self.fre = 0
        self.fkg = 0
