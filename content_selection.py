#content_selection.py
#Reads in a document and selects sentences to extract from the document
#for the summary
#Bobby Dorward and Ryan Wilson 11/30/16


#input will be a list of sentences
#sentences will be lists of words, which will be strings

import sys
import math
import counts
from collections import defaultdict
import collections
import nltk
import os
import parse_tree
sys.path.append('/pyStatParser-master/stat_parser')
#from nltk.parse

class selector:

	#stop = ["a","the","he","she","we","I","they","of", "an"]

	doc_counter = None
	word_counter=None
	word_map = None
	doc_count =0
	document = None
	summary = None
	parser_obj = None
	raw_parse_summary = None
	parse_summary = None

	current_pruned = None

	def __init__(self,doc_counter,word_counter,document):
		self.doc_counter = doc_counter
		self.word_counter = word_counter
		self.word_map = word_counter.get_word_map()
		self.doc_map = doc_counter.get_doc_map()
		self.doc_count = doc_counter.get_num_docs()
		self.document = document

		#self.printer(self.document.body)
		#print()
		print("Summary:")
		for j in self.document.title:
			print(j,end=" ")
		print()
		doc = self.document.body.copy()
		doc.sort(key=self.centrality,reverse=True)
		#for i in doc:
		#	print(self.centrality(i))
		best = doc[:max(1,int(0.1*len(document.body)))]
		best.sort(key=self.orig_order)
		self.printer(best)
		print()
		self.summary = best
		#self.parser_obj = GenericStanfordParser()
		

		#get parsetrees
		self.output_POS(best)
		os.system("javac *.java")
		os.system("java Parser POS_tmp")
		print(self.read_POS())
		print(best)
		self.raw_parse_summary = self.read_POS()

		os.system("rm *.class POS_tmp POS_tmp_parsed")
		print(parse_tree.parse_tree(self.raw_parse_summary[0]))
		print(parse_tree.parse_tree(self.raw_parse_summary[0]).get_sentence())
		ab= parse_tree.parse_tree(self.raw_parse_summary[0]).get_all_pruned_sentences()
		for a in ab:
			print(a)
		self.parse_summary = [parse_tree.parse_tree(raw) for raw in self.raw_parse_summary]
		self.prune()





	def tf(self,w,x):
		return self.word_map[w]
		#the count of how many times w occurs in x

	def idf(self,w):
		return math.log((self.doc_count+1)/(self.doc_map[w]+1))
		#log(N/n_w) where N is the total number of docs
		#and n_w is the number of docs with word w


	def tf_idf_cosine(self,x,y):

		#compute the weighted cosine between x and y 
		#page 771 jurafsky has formula
		#tf_{i,j} is number of times words j appears in doc i

		#iterate over words that are in both x and y
			#compute tf_{w,x}tf_{w,y}(idf_w)^2
		#divide that by: sqrt of sum over each freq count x_i of x
			#(tf_{x_i,x}idf_{x_i})^2
		#same with y
		total = 0
		#print("next")
		#print(x)
		#print(y)
		#print(self.intersection(x,y))
		#x = self.strip_stop(x)
		#y = self.strip_stop(y)
		for w in self.intersection(x,y):
			total+=self.tf(w,x)*self.tf(w,y)*(self.idf(w)**2)
		next_total = 0
		for w in x:
			next_total+=(self.tf(w,x)*self.idf(w))**2
		total = total/math.sqrt(next_total)
		next_total=0
		for w in y:
			next_total+=(self.tf(w,y)*self.idf(w))**2
		total = total/math.sqrt(next_total)
		return total

	def dot_product(self,x,y):
		total = 0
		for w in self.intersection(x,y):
			total+=self.tf(w,x)*self.tf(w,y)*(self.idf(w)**2)
		return total

	def intersection(self,x,y):
		return [w for w in x if w in y]

	def centrality(self,x):
		total = 0
		for sentence in self.document.body:
			total+=self.tf_idf_cosine(x,sentence)
		total=total/len(self.document.body)
		return total
	def centrality(self,x, doc = None):
		if doc == None:
			doc = self.document.body
		total = 0
		for sentence in doc:
			total+=self.tf_idf_cosine(x,sentence)
		total=total/len(doc)
		return total

	def centrality_cmp(self,x,y):
		return centrality(x)-centrality(y)
	def orig_order(self,x):
		return self.document.body.index(x)




	def printer(self, body):
		for i in body:
			print()
			print()
			for j in i:
				print(j,end=" ")

	def get_summary(self):
		return self.summary

	def parse(self, sentence):
		return self.parser_obj.parse(sentence)

	def output_POS(self, doc):
		output = open("POS_tmp", 'w')
		for sentence in doc:
			pos = nltk.pos_tag(sentence)
			for pair in pos:
				output.write(pair[0]+ " " + pair[1]+ " ")
			output.write("\n")
		output.close()

	def read_POS(self):
		lines = open("POS_tmp_parsed").readlines()
		return [ line[:-1] for line in lines]

	def get_raw_parse(self):
		return self.raw_parse_summary


	# def strip_stop(self,sentence):
	# 	ret = sentence.copy()
	# 	ret = [w for w in ret if not w in self.stop]
	# 	return ret


	# def prune(self):
	# 	ret = []
	# 	for tree in self.parse_summary:
	# 		phrases = []
	# 		ranked = []
	# 		tree.get_all_subtree_sentences(phrases)
	# 		for phrase in phrases:
	# 			ranked.append((self.centrality(phrase),phrase))
	# 		ranked.sort()
	# 		ret.append(ranked[0])
	# 	print(ret)
	# 	ret = [pair[1] for pair in ret]
	# 	self.printer(ret)


#first attempt at pruning
	def prune(self):
		self.current_pruned = []
		ret = []
		for tree in self.parse_summary:
			phrases = tree.get_all_pruned_sentences()
			ranked = []
			for phrase in phrases:
				ranked.append((math.log(len(phrase))*self.centrality(phrase),phrase))
			ranked.sort(reverse=True)
			#print(ranked)
			ret.append(ranked[0])
		ret = [pair[1] for pair in ret]
		self.printer(ret)
		return None

	# def prune_helper(self, cur_tree):
		
	# 	#try removing all children and compute centrality for each choice
	# 	#append choices and their score to current_pruned
	# 	# recurse on children

	# 	string = cur_tree.string
	# 	for c in cur_tree.children:
	# 		new_tree = parse_tree.parse_tree(string)
	# 		new_tree.children.remove(c)
	# 		print(new_tree.children)
	# 		sentence = new_tree.get_sentence()
	# 		print(sentence)
	# 		cent = self.centrality(sentence)




