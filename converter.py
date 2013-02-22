#!/usr/bin/env python
import sys

def convert(train, english, chinese, alignment):
	f_data = "%s.%s" % (train, chinese)
	e_data = "%s.%s" % (train, english)
	a_data = alignment
	
	sys.stderr.write("Converting paired alignments to the binary evaluation format...\n")
	bitext_lengths = [[len(sentence.strip().split()) for sentence in pair] for pair in zip(open(f_data), open(e_data))]
	index = 0
	for (l,alignments) in zip(bitext_lengths,open(a_data)):
		alignment_set = set([tuple(map(lambda x: int(x), pair.split('-'))) for pair in	alignments.split()])
		for s in range(l[0]):
			for t in range(l[1]):
				if (s,t) in alignment_set:
					sys.stdout.write('%d ' % index)
				index += 1
