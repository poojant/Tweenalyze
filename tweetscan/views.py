from django.http import HttpResponse
from tweetscan.forms import teamForm
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def activityHome(request):

	form = teamForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			hashtag = request.POST.get('hashtag', '')
			return redirect('/tweetscan/home?hashtag='+str(hashtag))
	else:
		hashtag_get = request.GET.get('hashtag')
		if hashtag_get is not None and hashtag_get != '':
			args = {'form': form,'hashtag': hashtag_get}

			#File: sentiment_mod.py
			import nltk
			import random
			#from nltk.corpus import movie_reviews
			from nltk.classify.scikitlearn import SklearnClassifier
			import pickle
			from sklearn.naive_bayes import MultinomialNB, BernoulliNB
			from sklearn.linear_model import LogisticRegression, SGDClassifier
			from sklearn.svm import SVC, LinearSVC, NuSVC
			from nltk.classify import ClassifierI
			from statistics import mode
			from nltk.tokenize import word_tokenize


			#i = 0
			class VoteClassifier(ClassifierI):
			    def __init__(self, *classifiers):
			        self._classifiers = classifiers

			    def classify(self, features):
			        votes = []
			        for c in self._classifiers:
			            v = c.classify(features)
			            votes.append(v)
			        return mode(votes)

			    def confidence(self, features):
			        votes = []
			        for c in self._classifiers:
			            v = c.classify(features)
			            votes.append(v)

			        choice_votes = votes.count(mode(votes))
			        conf = choice_votes / len(votes)
			        return conf


			documents_f = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/documents.pickle", "rb")
			documents = pickle.load(documents_f)
			documents_f.close()




			word_features5k_f = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/word_features5k.pickle", "rb")
			word_features = pickle.load(word_features5k_f)
			word_features5k_f.close()


			def find_features(document):
			    words = word_tokenize(document)
			    print(words)
			    features = {}
			    for w in word_features:
			        features[w] = (w in words)
			        #print(features[w])

			    return features



			featuresets_f = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/featuresets.pickle", "rb")
			featuresets = pickle.load(featuresets_f)
			featuresets_f.close()

			random.shuffle(featuresets)
			print(len(featuresets))

			testing_set = featuresets[10000:]
			training_set = featuresets[:10000]



			open_file = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/originalnaivebayes5k.pickle", "rb")
			classifier = pickle.load(open_file)
			open_file.close()


			open_file = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/MNB_classifier5k.pickle", "rb")
			MNB_classifier = pickle.load(open_file)
			open_file.close()



			open_file = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
			BernoulliNB_classifier = pickle.load(open_file)
			open_file.close()


			open_file = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
			LogisticRegression_classifier = pickle.load(open_file)
			open_file.close()


			open_file = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/pickled_algos/SGDC_classifier5k.pickle", "rb")
			SGDC_classifier = pickle.load(open_file)
			open_file.close()


			#open_file = open("/pickled_algos/LinearSVC_classifier5k.pickle", "rb")
			#LinearSVC_classifier = pickle.load(open_file)
			#open_file.close()




			voted_classifier = VoteClassifier(
			                                  classifier,
			                                  MNB_classifier,
			                                  BernoulliNB_classifier,
			                                  LogisticRegression_classifier)




			def sentiment(text):
			    print("inside sentiment")
			    feats = find_features(text)
			    #print(feats)
			    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
			    
			print("After senitment function loc")
			#Streaming Tweets
			from tweepy import Stream
			from tweepy import OAuthHandler
			from tweepy.streaming import StreamListener
			import json

			#consumer key, consumer secret, access token, access secret.
			ckey="lookB9U9DovzE29uvPBm9OV03"
			csecret="WJT4BPbyvWdEba3TfhRTBZZAw8JgHnj9bJGre4XOHvm0BOFs6o"
			atoken="3255426194-tv415MxWQSZlB4kxq4SQBQXhqNMnF54kwmxTfy5"
			asecret="MPHTzP2APFeu1o3mYMCLzt5EQFDo1oDNhqeoe5rEUqiRC"

			class listener(StreamListener):
			  
			  	def __init__(self):
			  		super().__init__()
			  		self.counter = 0
			  		self.limit = 5


			  	def on_data(self, data):
			    
				    #i=0
				    #while(i<10):
				    

				    all_data = json.loads(data)
				    tweet = all_data["text"]
				    #print(tweet)
				    #if all_data["created_at"] >
				    sentiment_value, confidence = sentiment(tweet)#Sentiment of Tweets
				    print(tweet, sentiment_value, confidence, self.counter)
				    self.counter+=1
				    if confidence*100 >= 80:
				    	output = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-text-out.txt","a")
				    	output.write(tweet)
				    	output.write('\n')
				    	output.close()
				    	output = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-out.txt","a")
				    	output.write(sentiment_value)
				    	output.write('\n')
				    	output.close()

#i+=1
				    if self.counter < self.limit:
				    	return True
				    else:
				    	twitterStream.disconnect()
				    return True

				    def on_error(self, status):
				    	print(status)
			  
			print("before twitterStream")
			open('C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-out.txt', 'w').close()    
			open('C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-text-out.txt', 'w').close()
			auth = OAuthHandler(ckey, csecret)
			auth.set_access_token(atoken, asecret)
			print("after auth")
			#print(word_tokenize("hello my name is Poojan"))
			i=0
			twitterStream = Stream(auth, listener())
			twitterStream.filter(track=[hashtag_get],languages=["en"])
			#Plotting Graphs of the sentiments 
			import matplotlib.pyplot as plt
			import matplotlib.animation as animation
			from matplotlib import style
			import time
			plt.rcdefaults()
			style.use("ggplot")

			fig = plt.figure()
			ax1 = fig.add_subplot(1,1,1)

			def animate(i):
			    pullData = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-out.txt","r").read()
			    lines = pullData.split('\n')

			    xar = []
			    yar = []

			    x = 0
			    y = 0

			    for l in lines[:]:
			        x += 1
			        if "pos" in l:
			            y += 1
			        elif "neg" in l:
			            y -= 1

			        xar.append(x)
			        yar.append(y)
			        
			    ax1.clear()
			    ax1.plot(xar,yar)
			ani = animation.FuncAnimation(fig, animate, interval=1000)
			#plt.show()
			plt.savefig("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/static/wordcloud.jpg")
			
			#wordcloud
			from wordcloud import WordCloud
			tweet=open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-text-out.txt","r")
			read_tweet=tweet.read()
			wordcloud = WordCloud(width=800,height=500,max_font_size=100,random_state=21).generate(read_tweet)
			plt.figure(figsize=(10, 7))
			plt.imshow(wordcloud, interpolation="bilinear")
			plt.axis('off')
			plt.title('WordCloud')
			plt.tight_layout()
			#plt.show()
			plt.savefig("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/static/wordcloud.jpg")


			#piechart
			pullData = open("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/outputs/twitter-out.txt","r").read()
			lines = pullData.split('\n')
			pos, neg = 0, 0
			for l in lines:
				if l == 'pos':
					pos += 1
				elif l == 'neg':
					neg += 1
			labels = ['positive','negative']
			sizes = [pos,neg]
			colors = ['#ff9999','#66b3ff']
			explode = [0.1,0]
			fig1, ax1 = plt.subplots()
			ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',shadow=True, startangle=90)
			ax1.axis('equal')
			plt.title('Sentiment Pie Chart')
			plt.tight_layout()
			#plt.show()
			plt.savefig("C:/Users/Poojan/Desktop/Projects/ETL Django/Tweenalyze/tweetscan/static/pie.jpg")
		else:
			args = {'form': form}
		
		return render(request, 'home.html', args)