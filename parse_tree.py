


class parse_tree :


	def __init__(self, parse_string) :
		self.children = []
		self.tag = ""
		self.isLex = True
		firstparens = True
		currentchildstring = ""
		currentchildparens = 0
		for symbol in parse_string[1:] :
			if firstparens :
				if symbol is '(' or symbol is ')' :
					currentchildparens += 1
					currentchildstring += symbol
					firstparens = False
					print(self.tag)
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
					print(self.tag, "is not lex")
					currentchildparens += 1
				else :
					currentchildstring += symbol


schemetree = "(dog(park(cat)(catdog))(catdogpark))"
print(schemetree)
parse_tree(schemetree)