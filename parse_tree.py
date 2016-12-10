


class parse_tree :


	def __init__(self, parse_string) :
		self.children = []
		self.tag = ""
		self.isLex = True
		self.string = parse_string
		firstparens = True
		currentchildstring = ""
		currentchildparens = 0
		for symbol in parse_string[1:] :
			if firstparens :
				if symbol is '(' or symbol is ')' :
					currentchildparens += 1
					currentchildstring += symbol
					firstparens = False
					#print(self.tag)
				else :
					self.tag += symbol
			else :
				if symbol is ')' :
					currentchildstring += symbol
					currentchildparens -= 1;
					if currentchildparens is 0 :
						self.children.append(parse_tree(currentchildstring))
						currentchildstring = ""
				elif symbol is '(' :
					currentchildstring += symbol
					self.isLex = False
					#print(self.tag, "is not lex")
					currentchildparens += 1
				else :
					currentchildstring += symbol
	def __str__(self):
		ret = "(" +self.tag
		for c in self.children:
			ret+= c.__str__()
		return ret + ")"

	def get_sentence(self):
		acc = []
		self.get_sentence_rec(acc)
		return acc
	def get_sentence_rec(self,acc):
		tag = self.tag.split()
		if len(tag)>1:
			acc.append(tag[1])
			return
		for c in self.children:
			c.get_sentence_rec(acc)

	def get_all_pruned_sentences(self):
		acc= []
		self.get_all_subtree_sentences(acc)
		ret = []
		sentence = self.get_sentence()
		for phrase in acc:
			matched = False
			for i,sentword in enumerate(sentence):
				matched= True
				for j,phraseword in enumerate(phrase):
					if sentence[i+j] != phrase[j] or i+j>len(sentence)-1:
						matched = False
						continue
				if matched:
					ret.append(sentence[0:i]+sentence[i+j:])
					break
		return ret



	def get_all_subtree_sentences(self,acc):
		if self.get_sentence() not in acc and len(self.get_sentence())>1:
			acc.append(self.get_sentence())
		for c in self.children:
			c.get_all_subtree_sentences(acc)




# schemetree = "(dog(park(cat)(catdog))(catdogpark))"
# print(schemetree)
# a= parse_tree(schemetree)
# print(a)