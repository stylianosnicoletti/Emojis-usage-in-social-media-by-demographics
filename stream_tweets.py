# Import from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# User credentials to access Twitter API 
access_token = '1044702510731206661-ZfLY0F4jquMLBRv0GZL0j4sNqOPMaS'
access_token_secret = 'f4WgiS8EopkfeonFuQGhgtqOssv3Tn10F64Q1gyxcY1jt'
consumer_key = '7gpuwvFvSYAkdRMkVUplTLDmz'
consumer_secret = '07sBb56KZ0tisy3cvRKxoMiDJ6jS5kbuOp9d2Ancz35Jgb03qn'

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    # Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

    # Capture tweet samples
	stream.sample()

