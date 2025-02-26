import logging
from typing import Optional, Dict, Any
import tweepy
from settings.config import ENV

class TwitterClient:
  def __init__(self):
    try:
      self.auth = tweepy.OAuth1UserHandler(
        consumer_key=ENV['API_KEY'],
        consumer_secret=ENV['API_SECRET_KEY'],
        access_token=ENV['ACCESS_TOKEN'],
        access_token_secret=ENV['ACCESS_TOKEN_SECRET']
      )

      self.client = tweepy.Client(
        ENV['BEARER_TOKEN'],
        ENV['API_KEY'],
        ENV['API_SECRET_KEY'],
        ENV['ACCESS_TOKEN'],
        ENV['ACCESS_TOKEN_SECRET']
      )

      self.api = tweepy.API(self.auth)

    except KeyError as e:
      logging.error(f"Missing environment variable: {str(e)}")
      raise
    except Exception as e:
      logging.error(f"Failed to initialize Twitter client: {str(e)}")
      raise

  def postTweet(self, status: str, filename: str) -> Optional[Dict[str, Any]]:
    """
    Post a tweet with media

    Args:
        status: Tweet text content
        filename: Path to media file

    Returns:
        Tweet response or None if failed
    """
    try:
      if not status or not filename:
        raise ValueError("Status and filename are required")

      logging.info(f"Uploading media: {filename}")
      media = self.api.media_upload(filename=filename)
      logging.info("Creating tweet with media")
      tweet = self.client.create_tweet(
        text=status,
        media_ids=[media.media_id]
      )

      logging.info("Tweet posted successfully")
      return tweet
    except tweepy.TweepyException as e:
      logging.error(f"Twitter API error: {str(e)}")
      raise
    except Exception as e:
      logging.error(f"Failed to post tweet: {str(e)}")
      raise

# Initialize Twitter client
twitter = TwitterClient()
postTweet = twitter.postTweet