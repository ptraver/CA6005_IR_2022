#TIMING
from datetime import datetime
global begin_time
begin_time = datetime.now()

#local module
import preprocessing

#other modules
from collections import Counter
from json import dump
from math import log, sqrt
from os import getcwd, listdir
from xml.etree.ElementTree import parse

# Global variables. When complete, idx and doc_dim_dict are exported for later use
directory = '/COLLECTION/'
idx = {}
doc_dim_dict = {}

# Export global variable idx to json
def export_idx():
	with open('VSM_idx.json', 'w') as fp:
		dump(idx, fp)

# Export global variable doc_dim_dict to json
def export_doc_dim_dict():
	with open('doc_dim_dict.json', 'w') as fp:
		dump(doc_dim_dict, fp)

# Join two strings on a whitespace
def collapse(headline, txt):
	# Try statement to avoid errors when either headline or article test is black
	try:
		return headline + ' ' + txt
	except (TypeError):
		return str(headline) + ' ' + str(txt)

# Take an xml collection file, return document ID and an amalaglamation of headline and article body
def parse_xml(fpath):

	root = parse(fpath).getroot()

	docid = root.find('DOCID').text
	headline = root.find('HEADLINE').text
	text = root.find('TEXT').text

	txt_list = preprocessing.tokenize(collapse(headline, text))

	return (docid, txt_list)

# Populates doc_dim_dict with the vector magnitude of each document
# Populates idx so that each collection document is a key. Within each document's entry, a dictionary gives the count of each of its words
def populate_idx(docid, txt_list):

	doc_dim = 0

	# find counts of word in txt_list
	counts = Counter(txt_list)

	# add frequency of each word into idx
	for word in counts:

		doc_dim += counts[word] ^ 2

		if word in idx:
			idx[word][docid] = counts[word]
		else:
			idx[word] = {docid: counts[word]}

	doc_dim_dict[docid] = sqrt(doc_dim)

# Parse an xml document, preprocess it and add it to idx
def add_doc_to_index(fpath):
	docid, txt_list = parse_xml(fpath)

	txt_list2 = preprocessing.preprocess(txt_list)
	populate_idx(docid, txt_list2)
	

if __name__ == "__main__":

	# set collection location
	path = getcwd() + directory

	# get names of all colleciton files
	fls = listdir(path)
	fls.pop(0)

	# loop over collection files, adding them to inverted index
	for filename in fls:
		add_doc_to_index(path + filename)

	# save idx as json
	export_idx()

	# save doc_dim_dict as json
	export_doc_dim_dict()

	# print timing stats
	print('VSM indexing timing: {}'.format(datetime.now() - begin_time))