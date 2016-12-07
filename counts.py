import os  
from collections import defaultdict
import re


#contains methods that count the number of documents each word occurs in
class doc_count:
	doc_map = defaultdict(int)     #map of word,count pairs where count is the
									#number of documents that word appears in
	docs = []						#list of documents which are lists of sentences
	N=0
	def __init__(self,folder,POS_flag):
		print("here")
		print('./'+folder)

		#read in files
		for fn in os.listdir('./'+folder):
			if fn == "CONTENTS" or fn=="README" or fn=="cats.txt" or fn[0]==".":
				continue
			print(fn)
			try:
				doc = document('./'+folder+'/'+fn)
				lines = doc.body
				self.docs.append(lines)
			except:
				continue
		self.fill_doc_map()

	def fill_doc_map(self):
		for doc in self.docs:
			self.N+=1
			words_in_doc = set()
			for sentence in doc:
				for word in sentence:
					words_in_doc.add(word)
			for word in words_in_doc:
				self.doc_map[word]+=1



	def get_doc_map(self):
		return self.doc_map

	def get_num_docs(self):
		return self.N

#contains methods to get counts of the words in the current document
class word_count:
	body = None
	word_map = defaultdict(int)
	def __init__(self,file,POS_flag):
		try:
			doc = document(file)
		except:
			print("faliure")
			exit(1)
		self.body = doc.body
		self.fill_word_map(self.body)

	def fill_word_map(self,doc):
		for sentence in doc:
			for word in sentence:
				self.word_map[word]+=1


	def get_word_map(self):
		return self.word_map



#represents a document, which has a title and a body
#the body is a list of sentences, which are themselves lists of words
class document:
	body = None
	title = None

	def __init__(self, file_name):
		file = open(file_name)
		self.initialize(file)

	def initialize(self,file):
		p = re.compile("\.\"?[\s]")
		self.title = file.readline().split()
		while self.title == []:
			self.title = file.readline().split()
		all_lines = file.read()
		split_lines = p.split(all_lines)
		lines = []
		for line in split_lines:
			line = line.split()
			if(len(line)>0):
				lines.append(line)
		self.body = lines





