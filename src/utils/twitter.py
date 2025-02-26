import tweepy
from settings.config import ENV

auth = tweepy.OAuth1UserHandler(
consumer_key=ENV['API_KEY'],
consumer_secret=ENV['API_SECRET_KEY'],
access_token=ENV['ACCESS_TOKEN'],
access_token_secret=ENV['ACCESS_TOKEN_SECRET']
)

client = tweepy.Client(
  ENV['BEARER_TOKEN'],
  ENV['API_KEY'],
  ENV['API_SECRET_KEY'],
  ENV['ACCESS_TOKEN'],
  ENV['ACCESS_TOKEN_SECRET']
)
api = tweepy.API(auth)

def postTweet(status,filename):
  try:
    media = api.media_upload(filename=filename)
    tweet = client.create_tweet(text=status, media_ids=[media.media_id])
    return tweet
  except Exception as e:
    print(e)


postTweet("Explore pixel art magic: Futuristic sunset cyberpunk scene 🌅🎮 #PixelArt","output_images/image_51821335-04ce-4eb1-8477-9cc47eabb9dc.png")