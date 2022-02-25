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

# LM hyperparameters
lm_lambda = 0.1
lm_lambda_comp = 1 - lm_lambda

# Global variables. When complete, idx is exported for later use
directory = '/COLLECTION/'
idx = {}

# Dictionary to record the total count of each word in the collection
total_freq = {}

# total number of words in the collection
global total_bag_size
total_bag_size = 0


# Export global variable idx to json
def export_idx():
	with open('LM_idx.json', 'w') as fp:
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

# Finds total bag size. Populates total_freq. Adds tf of each term to idx
def first_pass(docid, txt_list):

	global total_bag_size

	# length of document
	doc_len = len(txt_list)
	total_bag_size += doc_len

	# find counts of word in txt_list
	counts = Counter(txt_list)

	# add first_pass score for each word into idx
	for word in counts:
		if word in idx:
			idx[word][docid] = counts[word] / doc_len
			total_freq[word] += counts[word]
		else:
			idx[word] = {docid: counts[word] / doc_len}
			total_freq[word] = counts[word]

# Finish idx by applying unigram language model with Jelinek Mercer smothing throughout
def second_pass():
	for word in idx:
		for docid in idx[word]:
			tf = idx[word][docid]
			idx[word][docid] = log( 1 + ( (lm_lambda_comp * tf * total_bag_size) / (lm_lambda * total_freq[word]) ) )

# Parse an xml document, preprocess it and add it to idx
def add_doc_to_index(fpath):
	docid, txt_list = parse_xml(fpath)

	txt_list2 = preprocessing.preprocess(txt_list)
	first_pass(docid, txt_list2)
	
if __name__ == "__main__":

	# set collection location
	path = getcwd() + directory

	# get names of all colleciton files
	fls = listdir(path)
	fls.pop(0)

	# loop over collection files, adding them to inverted index
	for filename in fls:
		add_doc_to_index(path + filename)

	# complete the LM index with a second pass through idx
	second_pass()

	# save idx as json
	export_idx()

	# print timing stats
	print('LM indexing timing: {}'.format(datetime.now() - begin_time))