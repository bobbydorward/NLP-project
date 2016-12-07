#content_selection.py
#Reads in a document and selects sentences to extract from the document
#for the summary
#Bobby Dorward and Ryan Wilson 11/30/16


#input will be a list of sentences
#sentences will be lists of words, which will be strings

import math
import counts
from collections import defaultdict
import collections

class selector:

	#stop = ["a","the","he","she","we","I","they","of", "an"]

	doc_counter = None
	word_counter=None
	word_map = None
	doc_count =0
	document = None
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

	def intersection(self,x,y):
		return [w for w in x if w in y]

	def centrality(self,x):
		total = 0
		for sentence in self.document.body:
			total+=self.tf_idf_cosine(x,sentence)
		total=total/len(self.document.body)
		return total

	def centrality_cmp(self,x,y):
		return centrality(x)-centrality(y)
	def orig_order(self,x):
		return self.document.body.index(x)

	def __init__(self,doc_counter,word_counter,document):
		self.doc_counter = doc_counter
		self.word_counter = word_counter
		self.word_map = word_counter.get_word_map()
		self.doc_map = doc_counter.get_doc_map()
		self.doc_count = doc_counter.get_num_docs()
		self.document = document

		self.printer(self.document.body)
		print()
		print("summary")
		for j in self.document.title:
			print(j,end=" ")
		print()
		doc = self.document.body.copy()
		doc.sort(key=self.centrality,reverse=True)
		#for i in doc:
		#	print(self.centrality(i))
		best = doc[:max(1,int(0.25*len(document.body)))]
		best.sort(key=self.orig_order)
		self.printer(best)
		print()

	def printer(self, body):
		for i in body:
			print()
			print()
			for j in i:
				print(j,end=" ")

	# def strip_stop(self,sentence):
	# 	ret = sentence.copy()
	# 	ret = [w for w in ret if not w in self.stop]
	# 	return ret

			

