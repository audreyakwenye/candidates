import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize # Sentence Tokenizer
from nltk.tokenize import word_tokenize # Word Tokenizer
from nltk.probability import FreqDist
from .models import *
from .twitter import *

stop_words = ['i','me','my','myself','we''our','ours','ourselves',
            'you','your','yours','yourself','yourselves','he','him','his','himself',
            'she','her','hers','herself','it','its','itself','they','them','their',
            'theirs','themselves','what','which','who','whom','this','that','these',
            'those','am','is','are','was','were','be','been','being','have','has',
            'had','having','do','does','did','doing','a','an','the','and','but',
            'if','or','because','as','until','while','of','at','by','for','with',
            'about','against','between','into','through','during','before','after',
            'above','below','to','from','up','down','in','out','on','off','over',
            'under','again','further','then','once','here','there','when','where',
            'why','how','all','any','both','each','few','more','most','other','some',
            'such','no','nor','not','only','own','same','so','than','too','very',
            's','t','can','will','just','don','should','now','http','https','we','our', 'm', 't','us']

table = str.maketrans('','', string.punctuation)

def get_words(tweets):
        cleaned_listings = []
        for tweet in tweets:
            for i, listing in enumerate(tweets):
                tokens = word_tokenize(listing)
                lowercase_tokens = [w.lower() for w in tokens]
                no_punctuation = [x.translate(table) for x in lowercase_tokens]
                alphabetic = [word for word in no_punctuation if word.isalpha()]
                words = [w for w in alphabetic if not w in stop_words]
                cleaned_listings.extend(words)
                fdist = FreqDist(cleaned_listings)
            return(fdist.most_common(5))

def top_words(names):
    top_word = []
    for name in names:
      user = User.query.filter(User.name == name).one()
      tweets = [tweet.text for tweet in user.tweets]
      results = get_words(tweets)
      top_word.extend((name, results))
    return(top_word)