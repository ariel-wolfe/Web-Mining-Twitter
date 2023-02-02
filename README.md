# Web-Mining-Twitter

## Abstract
Web mining is a data mining topic that extracts information from web pages on the Internet. This data can used to show existing trends in large sections of information or trends specific to one user. Web mining can be very effective when it used on social media platforms. Social media can give insight on existing trends on the Internet just by looking into user accounts. What can be pulled from user accounts specifically can show their own interests based on data involving: following trends, common interests based on following, etc. This demonstration will show how web mining can utilized on a specific Twitter user account and show analytics that will display trends specific to the Twitter user being analyzed. 

## Motivation
The motivation for this project was primarily based on learning a new data mining topic and researching different applications and techniques of data mining. This course has covered different data mining techniques like Naïve Bayes, classification techniques, vector machines, Apriori algorithms, etc. Web mining is a topic that was not covered in this course that sparked the interest of the author to do a learning project on. 
Web mining covers on how to use data mining techniques specifically on how to extract information directly from the Web and using Web data to gain insight on current trends. There are three different techniques specific to web mining: web content mining, web structure mining, and web usage mining. All these three techniques are used for the purposes of web mining so that it improves several qualities if the Internet including: improving web search engines (Google, Bing, Yahoo, etc.), predict user behavior, and optimize e-services for specific webpages. This can be optimized in social media as well. Social media accounts can show information about specific users and any current trends based on what’s being posted on user accounts. 

## Existing Solutions
Web mining consists of three techniques: web content mining, web structure mining, and web usage mining. Theses technique all serve the over-arching purpose of web mining which is to gather useful information and improve web optimization. Each technique covers a specific part of web mining and track different parts of Internet-based trends. 

Web content mining is used for extracting information from web documents. The technique itself can be further broken down into two categories: search result mining and web page mining [1]. Web content is a broader definition for different data types: text, images, audio, etc. Web content mining optimizes extracting information from web pages that have content data based on common topics (forums, product descriptions). Web content mining functioning works as scanning and mining of web content according to the specific content being scanned. 

Web structure mining is defined as “the application of discovering structure information from the web” [2]. Web structure mining uses a data structure-based approach with graph theory where the application graphs are treated as nodes with the hyperlinks being treated like edges connecting any related web pages. The structure of a particular website shows the interconnectivity to other web pages through common nodes. Web structure mining optimizes the web mining by minimizing the amount of search results and indexing the amount of data available on the Internet. The purpose of web content mining is to identify the relationship between “web pages linked by information or direct link information” [2]. 

Web usage mining is used for primarily used for identifying and discovering usage patterns and trends within large datasets. The goal of web usage mining is to understand user behavior when looking at user access data on a common webpage. The types of behavior observed can include geographic location, the number of users that clicked on a common item in a webpage and the types of activities being done on the webpage [1]. Web usage mining collects data and analyzes them as logs, a simple data structure that represents append-only sequence of records. 

## Proposed Solutions
The proposed solution is a demonstration of web mining in use. In this demonstration, web mining will be used on various Twitter accounts and show basic analytics to demonstrate how using Twitter API can show a lot of insight about a specific user. This should several aspects when looking into a user account. When looking into basic analytics, this would show and compare account creation date, tweet rate, number of followers, location, statistics regarding following/followers, and tweets by day of the week and year. This demonstration will also utilize NLP techniques to investigate the following: user’s followers’ account creation, location of followers, and most used hashtags. 

## Implementation and Experiment
To access the Twitter webpage for data mining, the coder would need an API connection to Twitter’s database. An API (application programmable interface) is a software interface that allows services to other software applications. Python has a library called “tweepy” that helps developers access Twitter API, which would be used in the demo code. To access Twitter API via Python the developer would need the following: a Twitter account themselves, be in developer mode on Twitter’s web page, and have access credentials in the code. The access credentials are key as they are unique to each developer and is what allows the tweepy library to access Twitter’s API built-int functions. The credentials resemble the one’s in the following Figure.
![image](https://user-images.githubusercontent.com/124304251/216435652-b3d6f245-2cf2-4d30-96cb-f6bfa19646d7.png)
Figure 1. Twitter API access credentials in “credentials.yml”. 

With the credentials form Figure 1, the developer can access built-in functions in the tweepy library to pull data for the purposes of web mining. The experiment would tweepy and other Python libraries to pull data from a specific Twitter user account as a dataset and perform basic analytic and NLP algorithms. The credentials would be read in as a yaml file since the Python yaml library configures and stores the credentials for the demo code. 

The user Twitter account that will be used in the demo will have the account username read in using the API built-in functions. From there, the credentials will be verified and basic information (bio description if any, location if available, account creation date, and followers/accounts following) will be pulled from the account information and displayed in the output to verify the code is pulling the correct information from the specific user account. 

A caveat noticed in version 4.12 of tweepy is that there is not a built-in API function to pull a specific number of tweets, so a function was created to gather tweets and store them in a list array using the timeline function. The total number of tweets and tweet rate is displayed in the output and verified from the user account tweet number. Some follower statistics was generated in the demo. The number of followers was displayed along with the number of followers with a displayed location on their profiles. This information was used in a data frame and graphed. The account creation year of the user’s followers was gathered and used in a data frame graph. To expand on followers/following analytics, the average and median number of accounts followed per user follower was gathered as well as the average and median of followers per user follower, all displayed in the output. For analytics in the user tweets, the number of tweets by weekday and year was gathered and stored using a counter. This information was displayed and graphed. 

## Demo of Code
![image](https://user-images.githubusercontent.com/124304251/216436011-45c0f52e-4666-4c9d-a562-42c87a75f10e.png)

Figure 2. Twitter Account Used in Demo Code. 
```python
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
```
Figure 3. Files Imported for Demo Code. 

```python
# Twitter account
user_name = "@Colercw"
print("Twitter account: ", user_name)
print("Analysis date: ", date.today())
warnings.filterwarnings('ignore')
```
![image](https://user-images.githubusercontent.com/124304251/216437333-89e8dca9-cdeb-47bb-924e-63e433b45fc4.png)

Figure 4. Twitter Account Used Displayed with Analysis Date.

```python
# function def to read from yaml file
def get_from_yaml(yaml_path):
    with open(yaml_path) as f:
        yaml_file = f.read()
        result = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return result
```
Figure 5. Function Defined to Read in Yaml File. 

```python
# function to plot data frame
def plot_data(df, figure_size, x_point, y_point, title, color='blue', legend=None, x_label=None):
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

    plt.title(title, fontsize=15)
    plt.xlabel(y_point.capitalize())
    plt.ylabel(x_point.capitalize())
    plt.show()
```
Figure 6. Function Defined to Plot Data Frame.

```python
# def to gather location
def get_location(location):
    loc = ''

    location = location.strip()
    if location != '':
        tokens = location.split(',')
        loc = tokens[-1].strip()

    return loc
```
Figure 7. Function Defined to Gather Location.

```python
# connect to Twitter API
# read bot credentials
yaml_path = 'config/credentials.yml'
login_access = get_from_yaml(yaml_path)

# set up bot credentials
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
```
![image](https://user-images.githubusercontent.com/124304251/216438532-6b3dbb46-c910-4abf-9469-96db8018b5e9.png)

Figure 8. Setting Up and Authenticating API Credentials.

```python

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
```
![image](https://user-images.githubusercontent.com/124304251/216438718-3fa5f0d8-1680-4ace-b038-03c39c6fd741.png)

Figure 9. User Account Basic Information.

```python
# function retrieve tweets from user
def get_tweets(api, screen_name):
    tweets = []

    # request for most recent tweets
    try:
        new_tweets = api.user_timeline(count=1000)

        # save into tweets array
        tweets.extend(new_tweets)

        # save oldest tweet - 1
        oldest = tweets[-1].id - 1

        # retrieve tweets until none
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=1000, tweet_mode='extended', max_id=oldest)

            # save most recent tweets
            tweets.extend(new_tweets)

            # update id of oldest
            oldest = tweets[-1].id - 1
    except(socket.timeout) as e:
        print("Error: ", e)

    # make tweets into array with tweet's relevant field
    tweet_list = []
    for tweet in tweets:
        new_tweet = {
            'id': tweet.id_str,
            'created_at': tweet.created_at,
            'language': tweet.lang,
            'hashtags': [ht['text'] for ht in tweet.entities['hashtags']],
            'user_mentions': [mt['screen_name'] for mt in tweet.entities['user_mentions']],
            'retweet_count': tweet.retweet_count,
            'retweeted': tweet.retweeted,
        }
        tweet_list.append(new_tweet)

    return tweet_list
```
Figure 10. Function Defined to Retrieve Tweet List from User Account. 

```python
# gather tweet list from user
user_tweet_list = get_tweets(api, screen_name=user_name)
len(user_tweet_list)

# tweet number
tweet_list_num = [tweet for tweet in user_tweet_list if not tweet['retweeted']]
print("Total tweets: ", len(tweet_list_num))
```
![image](https://user-images.githubusercontent.com/124304251/216438940-ce2bccc6-1238-45d5-b6d2-f70565f772b5.png)

Figure 11. Displaying Total Number of Tweets

```python
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
```
![image](https://user-images.githubusercontent.com/124304251/216439196-182548b3-ee13-4ae3-977e-74209e32e9c5.png)

Figure 12. Statistics and Graph of Follower Account Creation Year.

```python
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
```
![image](https://user-images.githubusercontent.com/124304251/216439286-8fb5ac68-eca3-414d-b35f-a7807433954d.png)

Figure 13. Statistics and Graph of Follower Location.

```python
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
```
![image](https://user-images.githubusercontent.com/124304251/216439428-4f07ce4f-45c4-4383-96e9-47295edd8f34.png)

Figure 14. Basic Statistics of Following/Followers.

```python
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
```
![image](https://user-images.githubusercontent.com/124304251/216439544-04147ef8-d226-47f5-8aa9-5ce31f48d203.png)

Figure 15. Tweets by Weekday.

```python
# dataframe for tweets by year
df = pd.DataFrame.from_records(tweets_by_year.most_common(), columns=['year', 'frequency']).sort_values(by=['year'])

# plot tweets by year
x_point = 'year'
y_point = 'frequency'
title = 'Tweets by Year'
figure_size = (12, 10)
plot_data(df, figure_size, x_point, y_point, title)
```
![image](https://user-images.githubusercontent.com/124304251/216439687-d1d002ad-4fe6-4374-a756-2957ec14df22.png)

Figure 16. Tweets by Year.

```python
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
```
![image](https://user-images.githubusercontent.com/124304251/216439781-a224585d-5625-44d7-b0a5-04b2a5426299.png)

Figure 17. Hashtag Analytics in Output.

```python
# dataframe for most used hashtags (using top 15)
most_used_hashtags = hashtags_num.most_common(top_hashtags)
df = pd.DataFrame.from_records(most_used_hashtags, columns=['hashtag', 'frequency']).sort_values(by=['frequency'])

# plot dataframe
x_point = 'hashtag'
y_point = 'frequency'
title = "15 Most Used Hashtags"
figure_size = (12, 10)
plot_data(df, figure_size, x_point, y_point, title)
```
![image](https://user-images.githubusercontent.com/124304251/216439891-3f09622f-b79a-4682-ab7b-f0e1f506de60.png)

Figure 18. 15 Most Used Hashtags. 

## Discussion
The demo code showed the uses of primarily web content mining and web usage mining. There has been a lot of research to learn about Twitter API and how to navigate. The research included looking in Python reference libraries, watching tutorial videos, and seeing examples code in GitHub repositories. What has been shown in the demo code is basic statistics that was used from pulled data from the Twitter user account. This demo has shown how powerful certain web mining techniques and the tweepy library specifically can be.

## References 
1.	M. Opeyemi Samuel , “A Systematic Review of Current Trends in Web Content Mining,” iopscience, 2019. [Online]. Available: https://iopscience.iop.org/article/10.1088/1742-6596/1299/1/012040/pdf.  [Accessed: 06-Nov-2022]. 
2.	“Web Mining,” GeeksforGeeks, Jun. 27, 2019. https://www.geeksforgeeks.org/web-mining/ 
3.	“The Python Library Reference,” 2012. Accessed: Nov. 06, 2022. [Online]. Available: http://marvin.cs.uidaho.edu/Teaching/CS515/pythonLibrary.pdf 
4.	“Tweepy: Twitter for Python!,” GitHub, May 25, 2022. https://github.com/tweepy/tweepy 





