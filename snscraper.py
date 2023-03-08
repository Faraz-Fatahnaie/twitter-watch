import sys
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

[username, since] = sys.argv[1:]


def search(text, username, since, until, retweet, replies):
    q = text

    if username != '':
        q += f" from:{username}"

    if until == '':
        until = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    q += f" until:{until}"
    if since == '':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7)
                                           , '%Y-%m-%d')
    q += f" since:{since}"

    if retweet == 'y':
        q += f" exclude:retweets"
    if replies == 'y':
        q += f" exclude:replies"

    # FILE NAME
    if username != '' and text != '':
        filename = f"{since}_{until}_{username}_{text}.csv"
    elif username != "":
        filename = f"{since}_{until}_{username}.csv"
    else:
        filename = f"{since}_{until}_{text}.csv"
    return q


# Created a list to append all tweet attributes(data)
attributes_container = []
replies = []
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

query = search('', str(username), str(since), '', 'y', 'y')

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):

    attributes_container.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.replyCount,
                                 tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.inReplyToTweetId,
                                 tweet.conversationId])

    for j, reply in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{tweet.conversationId}').get_items()):
        replies.append([reply.date, reply.id, reply.rawContent, reply.user.username, reply.replyCount,
                        reply.retweetCount, reply.likeCount, reply.quoteCount, reply.inReplyToTweetId])

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

reply_df = pd.DataFrame(replies, columns=['DateTime', 'TweetId', 'Text', 'Username', 'ReplyCount',
                                          'RetweetCount', 'LikeCount', 'QuoteCount', '-'])

# Creating a dataframe from the tweets list above
print(attributes_container)
