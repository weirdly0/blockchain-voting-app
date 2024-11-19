
import tweepy

# Replace these values with your own
consumer_key = 'myrTDzfHDQGWxBXjaGEvFSWbH'
consumer_secret = 'EucTLDFop1Tg3yEU1p6aZTbMYooZhiVAyq8NsVCZQBdeWyJnKL'
access_token = '1858638649878855680-A7jiw0nZ0sCLaEqToYuHl9mK7aVf30'
access_token_secret = 'H3EpvbP3jzcHIii37p9rGNFWhgz8wckuDmodHRMSyyxbO'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHI1xAEAAAAAsBXuf%2BRl%2Fe0QHS7DW4QyP%2FQmkw8%3DMOUIM11VeXtuF04uesl6IqUxG40a0ShxWVcasoQF3e9KFLp9z0'  # Add your bearer token here

# Set up Tweepy Client for v2 API
client = tweepy.Client(bearer_token=bearer_token)
