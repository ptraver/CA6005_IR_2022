from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
symbols = ".\'\"1203456789;$:()"

# Take a string, split by whitespace and return as a list
def tokenize(docu):
	return docu.split()

# returns True if word is one character or less, otherwise False
def too_short(word):
	if len(word) <= 1:
		return True
	return False

# returns True if word contains any punctuation other than hyphen or underscore, otherwise False
def has_punctuation_or_numbers(word):
	
	for letter in word:
		if letter in symbols:
			return True
	return False

# Combines everything in this preprocessing script. Takes tokenized text, returns list after preprocessing operations
def preprocess(txt):
	return [stemmer.stem(w.lower()) for w in txt if not (too_short(w) or has_punctuation_or_numbers(w) or w.lower() in stop_words)]