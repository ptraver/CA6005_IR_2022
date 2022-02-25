#TIMING
from datetime import datetime
global begin_time
begin_time = datetime.now()

#local module
import preprocessing

#other modules
import collections, functools, operator

from json import load
from os import getcwd, listdir, remove
from os.path import exists
from sys import argv
from xml.etree.ElementTree import parse

# Global variables
directory = '/topics/'
trec_file = '{}_trec.txt'.format(argv[1]) #Must remember to delete it each time. Or else just sort out the code, better

# Load idx from json file
with open('{}_idx.json'.format(argv[1])) as json_file:
	idx = load(json_file)

# Take an xml topic file and return (queryid, title_list)
def parse_xml(fpath):

	root = parse(fpath).getroot()

	queryid = root.find('QUERYID').text
	title = root.find('TITLE').text

	# could draw on collapse as in script1 to combine title and desc
	title_list = preprocessing.tokenize(title)

	return (queryid, title_list)

# Takes a query and returns a dictionary giving all non-zero relevance scores by collection document
def query_dot_idx(query_id, title_list2):

	idx_terms = []

	for word in title_list2:
		if word in idx:
			idx_terms.append(idx[word])

	if not idx_terms:
		return {}
	elif len(idx_terms) == 1:
		return idx_terms[0]
	else:
		return dict(functools.reduce(operator.add, map(collections.Counter, idx_terms)))

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

	if exists('./{}'.format(trec_file)):
		remove('./{}'.format(trec_file))

	# loop over collection files, adding them to inverted index
	for filename in fls:
		score_collection(path + filename)

	# Print timing stats
	print('{} ranking timing: {}'.format(argv[1], datetime.now() - begin_time))