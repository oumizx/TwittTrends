
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boto3
import json
from pyes import *
#Enter your twitterAPI keys here
consumer_key = 'HeDMdrMZl1IRMundFMcY3c7hw'
consumer_secret = 'Smz8HNLqFiI8GMs6MGIJ21JJKe2Fs3D6R0R8S3KgievvgDSZG8'
access_token = '182386406-8Mhs3kxCnqDlAnE1n1YfavwyS8lgUFE836M6Zz0x'
access_secret = 'Z3eVU6UyrOPDifEWhYYy8zZH9levDmUbr5XLDrOHZ4pcf'

# Get the service resource
sqs = boto3.resource('sqs')
# Create/Get the SQS Queue instance
queue = sqs.get_queue_by_name(QueueName='twitttrends-17')
print(queue.url)

class StdOutListener(StreamListener):
    def on_data(self, data):
        data_json = json.loads(data)
        try:
            if data_json["coordinates"]:
                if data_json["lang"] == "en":
                    print(data_json['lang'])
                    coordinates = data_json['coordinates']['coordinates']
                    tweet = data_json['text']
                    place = data_json['place']
                    user_name = data_json['user']['name']
                    e_data = {
                        'User_name': {'DataType': 'String', 'StringValue': user_name},
                        'City': {'DataType': 'String', 'StringValue': place['full_name']},
                        'Country': {'DataType': 'String', 'StringValue': place['country']},
                        'Latitude': {'DataType': 'String', 'StringValue': str(coordinates[0])},
                        'Longitude': {'DataType': 'String', 'StringValue': str(coordinates[1])}
                    }
                    #
                    print(e_data)

                    response = queue.send_message(MessageBody=tweet, MessageAttributes=e_data)
                    print("Message ID " + str(response.get('MessageId')))
        except Exception as e:
            print('Exception ' + str(e))
        return True

    def on_error(self, status):
        print('error ' + str(status))


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, StdOutListener())
    stream.filter(locations=[-180, -90, 180, 90])

