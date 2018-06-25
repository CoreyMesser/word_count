import pandas as pd
import csv
import numpy as np
import sqlalchemy

from word_data.database import db_session as db
from word_data.database import engine as en
from word_data.models import Words

words = pd.read_sql_query('SELECT word, COUNT(1) FROM words GROUP BY word', en)
# words = pd.read_sql_table('words', en)
df = pd.DataFrame(words)
df.to_csv('/home/pibblefiasco/Development/word_count/words_data.csv')




# ORDER BY
#
