DROP TABLE if EXISTS words;

CREATE TABLE words
(
  id          INTEGER PRIMARY KEY     AUTOINCREMENT,
  words       TEXT                    NOT NULL,
  word_count  TEXT                    NOT NULL,
);