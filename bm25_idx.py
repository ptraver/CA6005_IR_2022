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

# BM25 hyperparameters
bm25_k = 1.2
bm25_b = 0.75

# Global variables. When complete, idx is exported for later use
directory = '/COLLECTION/'
idx = {}

# total number of words in the collection
global total_bag_size
total_bag_size = 0


# Export global variable idx to json
def export_idx():
	with open('BM25_idx.json', 'w') as fp:
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

# Finds total_bag_size. Stores count of each word in each document, and document length in idx
def first_pass(docid, txt_list):

	global total_bag_size

	# length of document
	doc_len = len(txt_list)
	# update total bag size
	total_bag_size += doc_len

	# find counts of word in txt_list
	counts = Counter(txt_list)

	# store (word frequency, doc length) for each word-document pair
	for word in counts:
		if word in idx:
			idx[word][docid] = (counts[word], doc_len)
		else:
			idx[word] = {docid: (counts[word], doc_len)}

# Takes total number of documents in collection and average docuemnt length, applies BM25 forumla to all values in idx
def second_pass(docN, avg_doc_len):
	for word in idx:
		docn_w_word = len(idx[word])
		for docid in idx[word]:
			wfreq_and_doc_len = idx[word][docid]
			# Apply BM25 formula
			idx[word][docid] = log((( docN - docn_w_word + 0.5) / docn_w_word + 0.5 ) + 1)  *  wfreq_and_doc_len[0] * (bm25_k + 1)  /  ( wfreq_and_doc_len[0] + (  bm25_k * (1 - bm25_b + bm25_b * (wfreq_and_doc_len[1] / avg_doc_len))) )

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

	# Find average document length
	docN = len(fls)
	avg_doc_len = total_bag_size / docN

	# complete the BM25 index with a second pass through idx
	second_pass(docN, avg_doc_len)

	# save idx as json
	export_idx()

	# print timing stats
	print('BM25 indexing timing: {}'.format(datetime.now() - begin_time))