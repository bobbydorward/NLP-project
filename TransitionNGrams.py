import sys
import counts
from collections import defaultdict


class transition_n_grams:

	folder = "reuters/training"
	document = "reuters/test/15549"
	ngramfrequencies = defaultdict(int)

	def __init__(self, documentcounts, document):
		docs = documentcounts.docs + document.body
		for doc in docs :
			prevline = None
			for line in doc :
				line = line[:-1]
				if prevline != None and len(prevline) != 0 and len(line) != 0:
					self.ngramfrequencies[(prevline[len(prevline)-1], line[0])] += 1
				prevline = line

	def order(self, summary) :
		transitionweights = defaultdict(int)
		for prevsentenceindex in range(len(summary)) :
			for nextsentenceindex in range(len(summary)) :
				if (prevsentenceindex != nextsentenceindex) :
					endword = summary[prevsentenceindex][-1]
					startword = summary[nextsentenceindex][0]
					freq = self.ngramfrequencies[(endword.lower(), startword.lower())]
					if freq == None :
						freq = 0
					transitionweights[(prevsentenceindex, nextsentenceindex)] = freq
		for prevsentenceindex in range(len(summary)) :
			for nextsentenceindex in range(prevsentenceindex+1, len(summary)) :
				if transitionweights[(prevsentenceindex, nextsentenceindex)] > transitionweights[(prevsentenceindex, prevsentenceindex+1)] :
					summary.insert(prevsentenceindex+1, summary[nextsentenceindex])
		print(transitionweights)

