# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 23:16:56 2020

@author: Suvarna
"""


import re 

import tweepy 

from tweepy import OAuthHandler 

from textblob import TextBlob 

import matplotlib.pyplot as plt

import pandas as pd

from wordcloud import WordCloud

consumer_key = 'IGYmZvT8Xz10ymoJsBPDz1ATV'
consumer_secret = 'pmRXJY0pulWLIU3x8AUFNpkfmFeopopV9XkITKJo2S9s9BikT3' 
access_token = '1055189598-rSoE79ejm5zgxdKGXF7wvsOynKbh2TiDuibavKK'
access_token_secret = 'DY8vV88gvgRHJBxTujay2uh9272FYZTrMydm7eISAHo4o'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

word = input("Enter the word here:")

filtered='word -filter:retweets'


tweets = tweepy.Cursor(api.search,
              q=filtered,
              lang="en").items(100)

tweets

cleantweets = [remove_url(tweet.text) for tweet in tweets]

sentiment_objects = [TextBlob(tweet) for tweet in cleantweets]

sentiment_objects[0].polarity, sentiment_objects[0]

sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

sentiment_values[0]

sentiment_values[0:99]

sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

sentiment_df

n=sentiment_df["polarity"]

m=pd.Series(n)

m

pos=0
neg=0
neu=0

for items in m:
    if items>0:
        print("Positive")
        pos=pos+1
    elif items<0:
        print("Negative")
        neg=neg+1
    else:
        print("Neutral")
        neu=neu+1
        
print(pos,neg,neu)

pieLabels=["Positive","Negative","Neutral"]

populationShare=[pos,neg,neu]

figureObject, axesObject = plt.subplots()

axesObject.pie(populationShare,labels=pieLabels,autopct='%1.2f',startangle=90)

axesObject.axis('equal')

plt.show()

print("%f percent twitter users feel positive about %s"%(pos,word))

print("%f percent twitter users feel negative about %s"%(neg,word))

print("%f percent twitter users feel neutral about %s"%(neu,word))

fig, ax = plt.subplots(figsize=(8, 6))

# Plot histogram of the polarity values
sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
             ax=ax,
             color="purple")

plt.title("Sentiments from the Tweets")
plt.show()


# Plot word cloud
all_words = ' '.join([text for text in cleantweets])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

