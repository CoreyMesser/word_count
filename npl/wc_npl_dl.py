# tokenization - given a text sequence tk is the task of breaking it into fragments separated with whitespaces. Certain
# characters are usually removed such as puctuations digits emoticons. These fragments are the so-called tokens used for
#     further processing.

# POS tagging, pos_tag(input_tokens)

# Named entities recognition, given a text sequence the task of named entities recognition is to location and identigy words or
# phrases that are of definitive categories such as names of persons, companies, and locations.

# Stemming and lemmatization is a process of reverting an inflected or derived word to its root form.  ex machine is the stem of machines

from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

