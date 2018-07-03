from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Paragraph(Base):
    __tablename__ = 'paragraph'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('paragraph_id_seq'::regclass)"))
    paragraph = Column(Text)
    paragraph_length_by_sentence = Column(Integer)
    paragraph_length_by_word = Column(Integer)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Words(Base):
    __tablename__ = 'words'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('words_id_seq'::regclass)"))
    sentence_id = Column(Integer, nullable=False)
    word = Column(Text, nullable=False)
    word_length = Column(Integer, nullable=False)
    syllables = Column(Integer, nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Sentence(Base):
    __tablename__ = 'sentence'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('sentence_id_seq'::regclass)"))
    paragraph_id = Column(ForeignKey('paragraph.id'), nullable=False)
    sentence = Column(Text, nullable=False)
    sentence_length = Column(Integer, nullable=False)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))

    paragraph = relationship('Paragraph')


class Dialogue(Base):
    __tablename__ = 'dialogue'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('dialogue_id_seq'::regclass)"))
    paragraph_id = Column(ForeignKey('paragraph.id'), nullable=False)
    dialogue = Column(Text, nullable=False)
    dialogue_length = Column(Integer, nullable=False)
    flesch_reading_ease = Column(Integer)
    flesch_kincaid_grade = Column(Integer)
    sentence_ids = Column(ForeignKey('sentence.id'), nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))

    paragraph = relationship('Paragraph')
    sentence = relationship('Sentence')
