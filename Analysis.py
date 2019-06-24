
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
from tkinter import * 
import matplotlib.pyplot as plt 

results=""
#slices=[3,3,3]

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'your-Consumer_key'
		consumer_secret = 'your-consumer_secret'
		access_token = 'your-access_token'
		access_token_secret = 'your acces token secret'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 


def function(name,count=10): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = name, count = count)
	

	results="" 

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
	p=100*len(ptweets)/len(tweets)
	print("Positive tweets percentage: {} %".format(p)) 
	#global results
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# picking neutral tweets from tweets 	
	neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 

	# percentage of negative tweets 
	n=100*len(ntweets)/len(tweets)
	

	print("Negative tweets percentage: {} %".format(n)) 

	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} %".format(100*(len(tweets)-(len(ptweets)+len(ntweets)))/len(tweets)))
	#print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ptweets)-len(ntweets))/len(tweets)))

	results=results+"Positive tweets %: "+str(p)+"\n"
	results=results+"Negative tweets %: "+str(n)+"\n"
	results=results+"Neutral tweets %: "+str(100-p-n)+"\n"
	result.set(results) 


	'''print("\n\nPositive tweets:") 
	for tweet in ptweets[:10]: 
		print(tweet['text'],"\n\n") '''

	'''print("\n\nNegative tweets:") 
	for tweet in ntweets[:10]: 
		print(tweet['text'],"\n\n") '''

	'''print("\n\nNeutral tweets:") 
	for tweet in neutweets[:10]: 
		print(tweet['text'],"\n\n")'''
	slices=[p,n,100-p-n]

	activities = ['positive', 'negative', 'neutral']  
	colors = ['r', 'y', 'g']
	plt.close()
	plt.pie(slices, labels = activities,colors=colors,startangle=90,shadow = True,explode=(0, 0, 0.1),radius = 1.2,autopct = '%1.1f%%') 
	plt.legend()
	plt.title("Tweeter Sentiment Analysis") 
	
	plt.show()  
	

if __name__ == "__main__": 
	master = Tk() 
	
	Label(master,text="TWEETER SENTIMENT ANALYSIS").grid(row=0, column=1)
	Label(master, text='Name of the Tweet').grid(row=2) 
	Label(master, text='Count of responses').grid(row=3) 
	name=StringVar()
	count=StringVar()

	e1 = Entry(master,textvariable=name) 
	e2 = Entry(master,textvariable=count) 
	e1.grid(row=2, column=1) 
	e2.grid(row=3, column=1) 
	submit=Button(master,text='Submit',fg='black',bg='yellow',command=lambda: function(name.get(),count.get()),height=1,width=7)
	submit.grid(row=4,column=3)
	result=StringVar()
	T = Label(master,textvariable=result).grid(row=5, column=1)
	
 
	#T.pack() 
	#T.set(results)
	#result.set(results)
	master.mainloop() 
