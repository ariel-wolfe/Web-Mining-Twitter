import socket
import tweepy
import numpy as np
import pandas as pd
import yaml
import calendar
import warnings
import time
from collections import Counter
from datetime import date
import matplotlib.pyplot as plt

# Twitter account
user_name = "@Colercw"
print("Twitter account: ", user_name)
print("Date Accessed: ", date.today())

warnings.filterwarnings('ignore')


# function def to read from yaml file
def get_from_yaml(yaml_path):
    with open(yaml_path) as f:
        yaml_file = f.read()
        file = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return file


# function to plot data frame
def plot_data(df, figure_size, x_point, y_point, graph_title, color='blue', legend=None, x_label=None):
    fig, ax = plt.subplots()
    df.plot.bar(ax=ax, x=x_point, y=y_point, color=color, alpha=0.75, figsize=figure_size)
    if legend:
        ax.legend(legend)
    else:
        ax.get_legend().remove()
    if x_label:
        x = np.arange(len(x_label))
        plt.xticks(x, x_label, rotation=45)
    else:
        plt.xticks(rotation=45)

    plt.title(graph_title, fontsize=10)
    plt.xlabel(y_point.capitalize())
    plt.ylabel(x_point.capitalize())
    plt.show()


# def to gather location
def get_location(location_on_acct):
    loc = ''

    location_on_acct = location_on_acct.strip()
    if location_on_acct != '':
        tokens = location_on_acct.split(',')
        loc = tokens[-1].strip()

    return loc


# connect to Twitter API
# read API credentials
yaml_path = 'config/credentials.yml'
login_access = get_from_yaml(yaml_path)

# set up API credentials
consumer_key = login_access['consumer_key']
consumer_secret = login_access['consumer_secret']
access_token = login_access['access_token']
access_token_secret = login_access['access_token_secret']

# authenticate access to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# create API object
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# show user details
user_account = api.get_user(screen_name=user_name)
print("User details: ")
print("Description: ", user_account.description)
print("Location: ", user_account.location)
print("Date Created: ", user_account.created_at)

# following/follower ratio
followers_num = user_account.followers_count
following_num = user_account.friends_count
print("Followers to Following:", followers_num, "folowers to ", following_num, "following.")


# function retrieve tweets from user
def get_tweets(api, screen_name):
    tweets = []

    # request for most recent tweets
    try:
        new_tweets = api.user_timeline(count=1000)

        # save into tweets array
        tweets.extend(new_tweets)

        # save oldest tweet - 1
        oldest_tweet = tweets[-1].id - 1

        # retrieve tweets until none
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=1000, tweet_mode='extended', max_id=oldest_tweet)

            # save most recent tweets
            tweets.extend(new_tweets)

            # update oldest tweet
            oldest_tweet = tweets[-1].id - 1
    except(socket.timeout) as e:
        print("Error: ", e)

    # make tweets into array with tweet's relevant field
    tweet_list = []
    for tweet in tweets:
        new_tweet_input = {
            'id': tweet.id_str,
            'created_at': tweet.created_at,
            'language': tweet.lang,
            'hashtags': [ht['text'] for ht in tweet.entities['hashtags']],
            'user_mentions': [mt['screen_name'] for mt in tweet.entities['user_mentions']],
            'retweet_count': tweet.retweet_count,
            'retweeted': tweet.retweeted,
        }
        tweet_list.append(new_tweet_input)

    return tweet_list


# gather tweet list from user
user_tweet_list = get_tweets(api, screen_name=user_name)
len(user_tweet_list)

# tweet number
tweet_list_num = [tweet for tweet in user_tweet_list if not tweet['retweeted']]
print("Total tweets: ", len(tweet_list_num))

# follower statistics
# list followers of selected user account
followers = []
for page in tweepy.Cursor(api.get_followers, screen_name=user_name, wait_on_rate_limit=True, count=200).pages():
    try:
        followers.extend(page)
    except tweepy.TweepError as e:
        time.sleep(10)

num_of_followers = len(followers)
print("Number of Followers: %s" % num_of_followers)

# follower info
# year of account creation
follower_acct_creation = Counter()
for flw in followers:
    created_at = flw.created_at.date()
    year = created_at.year
    follower_acct_creation[year] += 1

# follower dataframe
df = pd.DataFrame.from_records(follower_acct_creation.most_common(), columns=['year', 'frequency']).sort_values(
    by=['year'])

# plot years of follower account creation
figure_size = (12, 10)
x_point = 'year'
y_point = 'frequency'
title = 'Year of Follower Account Creation'
color = 'red'
plot_data(df, figure_size, x_point, y_point, title, color)

# follower location
flw_location = Counter()
for flw in followers:
    location = flw.location.strip()
    country = get_location(location)

    if country != '':
        flw_location[country] += 1

location_percentage = sum(flw_location.values()) / num_of_followers * 100
print("Number of followers with location:", round(location_percentage, 2), "%")

# follower location dataframe
df = pd.DataFrame.from_records(flw_location.most_common(), columns=['location', 'frequency'])
df = df.sort_values(by=['frequency'], ascending=False)

# plot follower location
x_point = 'location'
y_point = 'frequency'
title = 'Location of Followers'
figure_size = (12, 10)
plot_data(df, figure_size, x_point, y_point, title, color)

# statistics of following and followers
# year account was created
flw_following = []
flw_followers = []

for flw in followers:
    flw_following.append(flw.friends_count)
    flw_followers.append(flw.followers_count)

print("Accounts followed per followers: ")
print("Average: %.2f" % np.mean(flw_following))
print("Median: %.2f" % np.median(flw_following))

print("Number of followers of user followers: ")
print("Average: %.2f" % np.mean(flw_followers))
print("Median: %.2f" % np.median(flw_followers))

# tweets by day and year
tweets_by_year = Counter()
tweets_by_day = Counter()

for tweet in tweet_list_num:
    created_at = tweet['created_at'].date()
    weekday = created_at.weekday()
    year = created_at.year

    tweets_by_day[weekday] += 1
    tweets_by_year[year] += 1

# dataframe of tweets by day
df = pd.DataFrame.from_records(list(tweets_by_day.items()), columns=['weekday', 'frequency']).sort_values(
    by=['weekday'])
x = np.arange(7)
x_label = [calendar.day_name[d] for d in x]

# plot tweets by day
x_point = 'weekday'
y_point = 'frequency'
title = 'Tweets by Day'
figure_size = (12, 10)
color = 'red'
x_label = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plot_data(df, figure_size, x_point, y_point, title, color, None, x_label)

# dataframe for tweets by year
df = pd.DataFrame.from_records(tweets_by_year.most_common(), columns=['year', 'frequency']).sort_values(by=['year'])

# plot tweets by year
x_point = 'year'
y_point = 'frequency'
title = 'Tweets by Year'
figure_size = (12, 10)
plot_data(df, figure_size, x_point, y_point, title)

# most used hashtags in tweets
hashtags_num = Counter()
number_tweets = len(tweet_list_num)
top_hashtags = 15

for t in tweet_list_num:
    for ht in t['hashtags']:
        ht = '#' + ht.lower()
        hashtags_num[ht] += 1

print("Total used unique hashtags: %s" % len(hashtags_num))
print("Average hashtag per tweet: %.2f" % (sum(hashtags_num.values()) / number_tweets))

# dataframe for most used hashtags (using top 15)
most_used_hashtags = hashtags_num.most_common(top_hashtags)
df = pd.DataFrame.from_records(most_used_hashtags, columns=['hashtag', 'frequency']).sort_values(by=['frequency'])

# plot dataframe
x_point = 'hashtag'
y_point = 'frequency'
title = "15 Most Used Hashtags"
figure_size = (12, 10)
plot_data(df, figure_size, x_point, y_point, title)
