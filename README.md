# Getting Started
https://github.com/ptraver/CA6005_IR_2022
This README describes the steps needed to reproduce steps taken for the CA6005 information retrieval assignment 2022.

## Installation
The environment used to create the project is defined by requirements.txt. To mimic the environment run:

pip install -r requirements.txt

## Directory setup
These project files must sit in the same directory as /COLLECTION and /topics subdirectories. The scripts will look in these folders for collection and query documents respectively.

# Usage

## Indexing
The repository contains four scripts for indexing the contents of /COLLECTION:
vsm_idx.py, tf-idf_idx.py, bm25_idx.py, and LM_idx.py. Running these four scripts outputs json files vsm_idx.json, tf-idf_idx.json, bm25_idx.json, LM_idx.json respectively.

## Ranking
Scripts for ranking are rank_match.py and rank_cos_sim.py. Rank_match.py uses term-matching ranking, while rank_cos_sim.py uses cosine similarity ranking. Queries to be rank must sit in a /topics subdirectory. Usage requires a command line argument indicating which json to use as an index. For rank_match.py there are four options for the command line argument. These are:
python rank_match.py vsm
python rank_match.py tf-idf
python rank_match.py bm25
python rank_match.py LM

rank_cos_sim.py is designed only to be used in conjunction with vsm_idx.json, so the only way to run it is with the following command:
python rank_cos_sim.py vsm

Note that ranking scripts assume the relevant indexing script has already been run, and the necessary json file to load the index must already sit in the current directory.

Ranking scripts output a ‘trec’ file (VSM_trec.txt, tf-idf_trec.txt, BM25_trec.txt and LM_trec.txt). NOTE: in the case of vsm, the outputted ‘trec’ file will have the same name irrespective of whether it has been produced with rank_match.py or rank_cos_sim.py. This ‘trec’ file is in the required format to be evaluated using trec_eval.  

# Contact
Patrick Travers – Patrick.travers3@mail.dcu.ie
Project Link: https://github.com/ptraver/CA6005_IR_2022
