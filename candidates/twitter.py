import tweepy
from .models import DB, Tweet, User
from decouple import config

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                    config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                                config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    """Add or update a user *and* their Tweets, error if no/private user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # We want as many recent non-retweet/reply statuses as we can get
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], time=tweet.created_at)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()

def get_trending():
    results = TWITTER.trends_place(id = 23424977)
    trends = []
    for location in results:
        for trend in location["trends"]:
          trend = trend["name"]
          trends.append(trend)
    return(trends)  

def compare_trending(names, trends):
    topic_tweets = []
    for name in names:
      user = User.query.filter(User.name == name).one()
      tweets = [tweet.text for tweet in user.tweets]
      for tweet in tweets:
        for trend in trends:
          if trend in tweet:
            i = tweet
            total = (name, i)
            topic_tweets.append(total)
    return(topic_tweets)


def compare_topics(names, topics):
    topic_tweets = []
    for name in names:
      user = User.query.filter(User.name == name).one()
      tweets = [tweet.text for tweet in user.tweets]
      for tweet in tweets:
        if topics in tweet:
          i = tweet
          total = (name, i)
          topic_tweets.append(total)
    return(topic_tweets)

def compare_names(names):
    topic_tweets = []
    for name in names:
      user = User.query.filter(User.name == name).one()
      tweets = [tweet.text for tweet in user.tweets]
      for tweet in tweets:
        for name1 in names:
          if name1 in tweet:
            i = tweet
            total = (name, i)
            topic_tweets.append(total)
    return(topic_tweets)


