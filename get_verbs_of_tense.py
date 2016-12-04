import nltk
a = nltk.corpus.brown.tagged_words()
def get_all_words(tense, dest_name):
	f = open(dest_name, 'w')
	set_words = set()
	for elem in a:
		if str(elem[1]) == tense:
			word = str(elem[0]).lower()
			if word not in set_words:
				f.write(word)
				f.write('\n')
				set_words.add(word)
	f.close()