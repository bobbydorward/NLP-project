
import content_selection
import counts

def main():

	folder = "reuters/training"
	#document = "reuters/test/14890"
	document = "nytimestest"
	doc_count = counts.doc_count(folder,False)
	word_count = counts.word_count(document,False)
	document = counts.document(document)
	selector = content_selection.selector(doc_count,word_count,document)


if __name__=='__main__':
	main()