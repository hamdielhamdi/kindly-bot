import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
import numpy as np

"""
This class will mesure similarity base on  2 basic  methods
one : Convert a collection of raw documents to a matrix of TF-IDF features.
two : Levenshtein Distance
"""

# to be sure, download it only one time   
def loading_punk() : 
	if "already_loaded" not in globals():
		globals().update({"already_loaded" : True})
		nltk.download('punkt')
		return True 
	return False

class SimilarityMesure:
	def __init__(self, threash):
		# initiate a stemmer
		loading_punk()
		self.threash = threash
		self.stemmer = nltk.stem.porter.PorterStemmer()
		self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

	# get stem
	def stem_tokens(self,tokens):
	    return [self.stemmer.stem(item) for item in tokens]

	#remove punctuation, lowercase, stem
	def normalize(self,text):
		return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))

	def vectorize(self):
		#Convert a collection of raw documents to a matrix of TF-IDF features
		return  TfidfVectorizer(tokenizer=self.normalize,min_df  =0.1)

	# calculate similarity between 2 phrase
	def similarity(self,text1, text2):
	    tfidf = self.vectorize().fit_transform([text1, text2])
	    return ((tfidf * tfidf.T).A)[0,1]

	def sort_list_dict(self, ld, key):
		return sorted(ld, key=itemgetter(key), reverse=True)

	# check one phrase against all
	# O(n) complexity
	def mesure_sim(self, base, model_list):
		# mesure similarity 
		mesure = [{'mesure':self.similarity(base, val),'phrase':val} for val in model_list]
		# sort data 
		newlist =  self.sort_list_dict(mesure, 'mesure')
		# check if mesure > threash hold
		if float(newlist[0]['mesure']) > self.threash:
			return newlist[0]
		return None
