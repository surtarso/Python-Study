## pip install tweepy
import tweepy

##----------------------------------------------------------------- keys and auth
# API keyws that yous saved earlier
api_key = "..."
api_secrets = "..."
access_token = "..."
access_secret = "..."
 
# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')


##------------------------------------------------------------------ overview of requests
user = api.get_user('ChouinardJC') # Store user as a variable
 
# Get user Twitter statistics
print(f"user.followers_count: {user.followers_count}")
print(f"user.listed_count: {user.listed_count}")
print(f"user.statuses_count: {user.statuses_count}")
 
# Show followers
for follower in user.followers():
    print('Name: ' + str(follower.name))
    print('Username: ' + str(follower.screen_name))
 
# Follow a user
api.create_friendship('ChouinardJC')
 
# Get tweets from a user tmeline
tweets = api.user_timeline(id='ChouinardJC', count=200)
tweets_extended = api.user_timeline(id='ChouinardJC', tweet_mode='extended', count=200)
print(tweets_extended)
 
# Like or retweet tweets
id = 'id_of_tweet' # tweet ID
tweet = api.get_status(id) # get tweets with specific id
tweet.favorite() # Like a tweet
tweet.retweet() # Retweet


##----------------------------------------------------------- Get Tweets and Understand the JSON Response
# Get a list of tweets
tweets = api.user_timeline(id='ChouinardJC', count=200)
tweets_extended = api.user_timeline(id='ChouinardJC', tweet_mode='extended', count=200)
 
# Show one tweet's JSON
tweet = tweets[0]
tweet._json

##----------------------------------------------------------- a few functions to parse Twitter API’s JSON
# Get tweet data
print(f'Created at:{tweet.created_at}')
print(f'Tweet id:{tweet.id}')
 
# Get tweet text
try:
    print(f'Tweet text:{tweet.text}')
except:
    # Get tweet text in extended mode
    print(f'Tweet text:{tweet.full_text}')
 
# Get tweet status
print(f'Is Retweeted:{tweet.retweeted}')
print(f'Is favorited:{tweet.favorited}')
print(f'Is quote:{tweet.is_quote_status}')
 
# Get Tweet statistics
print(f'Retweet count:{tweet.retweet_count}')
print(f'Favorite count:{tweet.favorite_count}')
 
# Get tweet lang
print(f'Tweet lang:{tweet.lang}')
 
# Get replied to
print(f'In reply to status id:{tweet.in_reply_to_status_id}')
print(f'In reply to user id:{tweet.in_reply_to_user_id}')