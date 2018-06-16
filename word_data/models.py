from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dialogue(Base):
    __tablename__ = 'dialogue'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('dialogue_id_seq'::regclass)"))
    dialogue = Column(Text, nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Paragraph(Base):
    __tablename__ = 'paragraph'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('paragraph_id_seq'::regclass)"))
    paragraph = Column(Text)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Sentence(Base):
    __tablename__ = 'sentence'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('sentence_id_seq'::regclass)"))
    sentence = Column(Text, nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))


class Word(Base):
    __tablename__ = 'word'
    __table_args__ = (
        CheckConstraint("date_part('timezone'::text, created_at) = '0'::double precision"),
        CheckConstraint("date_part('timezone'::text, updated_at) = '0'::double precision")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('word_id_seq'::regclass)"))
    word = Column(Text, nullable=False)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("now_utc()"))
