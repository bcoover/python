# perform text sentiment analysis based on heuristic training
import nltk
import urllib

from nltk.probability import FreqDist, ELEProbDist


from nltk.classify.util import apply_features,accuracy


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words
    
def get_word_features(wordlist):
    wordlist = FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
    
 
pos_tweets=[('I love this car','positive'), 
('This view is amazing','positive'),
('I feel great this morning','positive'),
('I am so excited about the concert','positive'),
('He is my best friend','positive')]

neg_tweets=[('I do not like this car','negative'),
('This view is horrible','negative'),
('I feel tired this morning','negative'),
('I am not looking forward to the concert','negative'),
('He is my enemy','negative')]

tweets=[]
for(words,sentiment)in pos_tweets+neg_tweets:
  words_filtered=[e.lower() for e in words.split() if len(e)>=3]
  tweets.append((words_filtered,sentiment))

test_pos_tweets=[('I feel happy this morning','positive'), 
('Larry is my friend','positive')]

test_neg_tweets=[('I do not like that man','negative'),
('This view is horrible','negative'),
('The house is not great','negative'),
('Your song is annoying','negative')]

test_tweets=[]
for(test_words,test_sentiment)in test_pos_tweets+test_neg_tweets:
  test_words_filtered=[e.lower() for e in test_words.split() if len(e)>=3]
  test_tweets.append((test_words_filtered,test_sentiment))
  
    
word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    return features       
                       
    
training_set = apply_features(extract_features, tweets)

test_training_set=apply_features(extract_features, test_tweets)

classifier = nltk.classify.NaiveBayesClassifier.train(training_set)

#input to evaluate

#example 1: from web
#from urllib import urlopen
#url = "http://www.gutenberg.org/files/2554/2554.txt"
#raw = urlopen(url).read()
#tweet = raw

#example 2: from file
#f = open('/Users/brett/Dropbox/Personal/Resumes/Brett Coover - Resume - June 2010.txt', 'r')
#tweet = []
#for line in f:
#    tweet.append(line)
#tweet = str(tweet)

#example 3: basic text
tweet = 'I am excited because your song is great and amazing'

#evaluate
sentiment = classifier.classify(extract_features(tweet.split()))
accuracy = nltk.classify.util.accuracy(classifier,test_training_set)

#Show output
classifier.show_most_informative_features(10)
print '\n' + 'Accuracy: ' + str(accuracy * 100)[:4] + ' %' + '  (' + str(accuracy) + ')' + '\n'
print 'Sentiment: ' + sentiment + '\n'
