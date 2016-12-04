import os  
from collections import defaultdict
import re
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
			file = open('./'+folder+'/'+fn)
			lines = []
			try:
				all_lines = file.read()
				split_lines = all_lines.split(".")
				for line in split_lines:
					line = line.split()
					if(len(line)>0):
						lines.append(line)
						#print(line)
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


class word_count:
	document = None
	word_map = defaultdict(int)
	def __init__(self,file,POS_flag):
		f = open(file)
		lines = None
		if(POS_flag):
			lines = self.POS_read(f)
		else:
			lines = self.normal_read(f)
		self.document = lines
		self.fill_word_map(lines)

	def POS_read(self,file):
		lines = []
		for line in file:
			line = line.split()
			line = [re.match("(.+)/", word).group(1) for word in line]
			if(len(line)>0):
				lines.append(line)
		return lines

	def normal_read(self,file):
		lines = []
		all_lines = file.read()
		split_lines = all_lines.split(".")
		print(split_lines)
		for line in split_lines:
			print(line.split())
			line = line.split()
			if(len(line)>0):
				lines.append(line)
		return lines

	def fill_word_map(self,doc):
		for sentence in doc:
			for word in sentence:
				self.word_map[word]+=1

	def get_word_map(self):
		return self.word_map

	def get_document(self):
		return self.document




