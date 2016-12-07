import sys
import counts
from collections import defaultdict


class transition_n_gram:

	folder = "reuters/training"
	document = "reuters/test/15549"

	def __init__(self, documentcounts):
		self.docs = documentcounts.docs
		self.ngramfrequencies = {}
		for doc in self.docs :
			prevline = None
			for line in doc :
				if prevline != None :
					ngramfrequencies[(prevline[len(prevline)-1], line[0])] += 1
				prevline = line

	def order()


