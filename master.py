
import content_selection
import counts
import TransitionNGrams
import sys

def main():

	folder = "OANC-GrAF/all"
	document = "reuters/test/14890"
	document = "OANC-GrAF/Budapest-History.txt"
	if len(sys.argv) > 1 :
		document = sys.argv[1]
	doc_count = counts.doc_count(folder,False)
	word_count = counts.word_count(document,False)
	document = counts.document(document)
	selector = content_selection.selector(doc_count,word_count,document)
	TransitionNGrams.transition_n_grams(doc_count, document).order(selector.summary)


if __name__=='__main__':
	main()