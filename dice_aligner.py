#!/usr/bin/env python
import sys
from collections import defaultdict

# Default threshold: 0.5, num_sents = sys.maxint
def align(train, english, chinese, threshold, num_sents):
	f_data = "%s.%s" % (train, chinese)
	e_data = "%s.%s" % (train, english)
	
	sys.stderr.write("Training with Dice's coefficient...")
	bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:num_sents]]
	f_count = defaultdict(int)
	e_count = defaultdict(int)
	fe_count = defaultdict(int)
	for (n, (f, e)) in enumerate(bitext):
		for f_i in set(f):
			f_count[f_i] += 1
			for e_j in set(e):
				fe_count[(f_i,e_j)] += 1
		for e_j in set(e):
			e_count[e_j] += 1
		if n % 500 == 0:
			sys.stderr.write(".")
	
	dice = defaultdict(int)
	for (k, (f_i, e_j)) in enumerate(fe_count.keys()):
		dice[(f_i,e_j)] = 2.0 * fe_count[(f_i, e_j)] / (f_count[f_i] + e_count[e_j])
		if k % 5000 == 0:
			sys.stderr.write(".")
	sys.stderr.write("\n")
	
	for (f, e) in bitext:
		for (i, f_i) in enumerate(f): 
			for (j, e_j) in enumerate(e):
				if dice[(f_i,e_j)] >= threshold:
					sys.stdout.write("%i-%i " % (i,j))
		sys.stdout.write("\n")
