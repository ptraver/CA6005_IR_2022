#TIMING
from datetime import datetime
global begin_time
begin_time = datetime.now()

#local module
import preprocessing

#other modules
import collections, functools, operator

from json import load
from math import sqrt
from os import getcwd, listdir, remove
from os.path import exists
from sys import argv
from xml.etree.ElementTree import parse

# Global variables
directory = '/topics/'
trec_file = '{}_trec.txt'.format(argv[1])


# Load idx from json file
with open('{}_idx.json'.format(argv[1])) as json_idx:
	idx = load(json_idx)

# Load doc_dim_dict from json file
with open('doc_dim_dict.json') as json_dict:
	doc_dim_dict = load(json_dict)

# Take an xml topic file and return (queryid, title_list)
def parse_xml(fpath):

	root = parse(fpath).getroot()

	queryid = root.find('QUERYID').text
	title = root.find('TITLE').text

	title_list = preprocessing.tokenize(title)

	return (queryid, title_list)

# Normalise dot product by dividing by the product of the vector magnitudes
def normalise(value, query_dim, key):
	return value / (query_dim * doc_dim_dict[key])

# Completes cosine similarity score for all values in idx
def query_dot_idx(query_id, title_list2):

	idx_terms = []
	query_dim = 0

	# find counts of word in txt_list
	counts = collections.Counter(title_list2)

	for word in counts:

		freq_in_query = counts[word]
		query_dim += freq_in_query ^ 2

		if word in idx:
			temp_dict = {}
			for key, value in idx[word].items():
				temp_dict[key] = value * freq_in_query
			idx_terms.append(temp_dict)

	query_dim = sqrt(query_dim)

	if not idx_terms:
		return {}
	elif len(idx_terms) == 1:
		for key, value in idx_terms[0].items():
			idx_terms[0][key] = normalise(value, query_dim, key)
		return idx_terms[0]
	else:
		collapsed_dict = dict(functools.reduce(operator.add, map(collections.Counter, idx_terms)))

		for key, value in collapsed_dict.items():
			collapsed_dict[key] = normalise(value, query_dim, key)
		return collapsed_dict

# Function for testing purposes
def display_results(resultant):
	print(sorted( ((v,k) for k,v in resultant.items()), reverse=True))

# Add a document-query relevance score to teh relevant output file
def trec_results(resultant, query_id):

	with open(trec_file, 'a') as vsm_trec:
		for count, value in enumerate(sorted( ((v,k) for k,v in resultant.items()), reverse=True)):
			vsm_trec.write('{} 0 {} {} {} {}\n'.format(query_id, value[1], count, value[0], argv[1]))

# Takes a query and calculates relevance for all colleciton documents
def score_collection(fpath):
	query_id, title_list = parse_xml(fpath)

	title_list2 = preprocessing.preprocess(title_list)

	resultant = query_dot_idx(query_id, title_list2)

	trec_results(resultant, query_id)

if __name__ == "__main__":

	# set collection location
	path = getcwd() + directory

	# get names of all collection files
	fls = listdir(path)
	fls.pop(0)

	# If the file to record relevance already exists, remove it
	if exists('./{}'.format(trec_file)):
		remove('./{}'.format(trec_file))

	# loop over collection files, adding them to inverted index
	for filename in fls:
		score_collection(path + filename)

	# Print timing stats
	print('{} ranking timing: {}'.format(argv[1], datetime.now() - begin_time))