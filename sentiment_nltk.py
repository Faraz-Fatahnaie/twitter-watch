import sys
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_nltk(text):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.rawContent)

    if score['neg'] > score['pos']:
        return 0
    elif score['pos'] > score['neg']:
        return 1
    elif score['pos'] == score['neg']:
        return -1
    else:
        return None


if __name__ == "__main__":
    # Created a list to append all tweet attributes(data)
    attributes_container = []
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    query = "from: elonmusk"
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):

        attributes_container.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.replyCount,
                                     tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.inReplyToTweetId])

        tweet_list.append(tweet.rawContent)
        analysis = TextBlob(tweet.rawContent)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.rawContent)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity

        if neg > pos:
            negative_list.append(tweet.rawContent)
            attributes_container.append('negative')
            negative += 1
        elif pos > neg:
            positive_list.append(tweet.rawContent)
            attributes_container.append('positive')
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet.rawContent)
            attributes_container.append('neutral')
            neutral += 1

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(attributes_container, columns=['DateTime', 'TweetId', 'Text', 'Username', 'ReplyCount',
                                                            'RetweetCount', 'LikeCount', 'QuoteCount', '-'])

    # Creating a dataframe from the tweets list above
    print(attributes_container)
