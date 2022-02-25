#TIMING
from datetime import datetime
global begin_time
begin_time = datetime.now()

#local module
import preprocessing

#other modules
from collections import Counter
from json import dump
from math import log
from os import getcwd, listdir
from xml.etree.ElementTree import parse

# Global variables. When complete, idx is exported for later use
directory = '/COLLECTION/'
idx = {}

# Export global variable idx to json
def export_idx():
	with open('tf-idf_idx.json', 'w') as fp:
		dump(idx, fp)

# Join two strings on a whitespace
def collapse(headline, txt):
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

# Take a txt_list and add tf scores to the idx dictionary
def tf(docid, txt_list):

	# find counts of word in txt_list
	counts = Counter(txt_list)

	# add tf score for each word into idx
	for word in counts:
		if word in idx:
			idx[word][docid] = counts[word] / len(txt_list)
		else:
			idx[word] = {docid: counts[word] / len(txt_list)}

# Multiply all tf scores idx by idf
def idf(docn):
	for word in idx:
		ln = len(idx[word])
		for docid in idx[word]:
			idx[word][docid] *= log(docn / ln)

# Parse an xml document, preprocess it and add it to idx
def add_doc_to_index(fpath):
	docid, txt_list = parse_xml(fpath)

	txt_list2 = preprocessing.preprocess(txt_list)
	tf(docid, txt_list2)
	
if __name__ == "__main__":

	# set collection location
	path = getcwd() + directory

	# get names of all colleciton files
	fls = listdir(path)
	fls.pop(0)

	# loop over collection files, adding them to inverted index
	for filename in fls:
		add_doc_to_index(path + filename)

	# complete the tf-idf index by multiplying the idf factor throughout
	idf(len(fls))

	# save the tf-idf index as 'tf-idf_idx.json'
	export_idx()

	# print timing stats
	print('tf-idf indexing timing: {}'.format(datetime.now() - begin_time))