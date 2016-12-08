/*
  TaggedWord

  This class represents a tagged word for use with POS tagging applications.

  A tagged word consists of a word and a tag.
*/

/* You may add methods to this class */
public class TaggedWord {
    private String word;
    private String tag;

    public TaggedWord(String word, String tag){
	this.word = word;
	this.tag = tag;
    }

    public String getWord(){
	return word;
    }

    public String getTag(){
	return tag;
    }

    public String toString(){
	return word + '/' + tag;
    }
}

