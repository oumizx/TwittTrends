import time
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
from kafka import KafkaConsumer
import boto3
import json


sns = boto3.client('sns', region_name='us-west-2')
arn = 'arn:aws:sns:us-west-2:661110844100:Tweet_topic_notification'
consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

class Analyzer:
    def __init__(self):
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2017-02-27',
            username='43948587-5a8a-49ec-a3c0-84ad295f573c',
            password='kfUtl8XAVmQs')

    def sentiment(self, textinput):
        response = self.nlu.analyze(
            text=textinput,
            features=[features.Sentiment()])
        result = response['sentiment']['targets']['label']
        print(result)
        return result


a = Analyzer()


def worker():
    for message in consumer:
        print("hahahah")
        try:
            msg = json.loads(message.value.decode('utf-8'))
            tweet = msg['Tweet']['StringValue']
            user_name = msg['User_name']['StringValue']
            city = msg['City']['StringValue']
            country = msg['Country']['StringValue']
            lat = msg['Latitude']['StringValue']
            lng = msg['Longitude']['StringValue']
            print(tweet)
            try:
                sentiment = a.sentiment(tweet)
            except Exception as e:
                print(e)
                sentiment = "neutral"

            sns_message = {"user_name": user_name, "tweet": tweet, "city": city, "country": country, "lat": lat,
                           "lng": lng,
                           "sentiment": sentiment}
            print("SNS messsage: " + str(sns_message))

            sns.publish(
                TargetArn=arn,
                Message=json.dumps(sns_message)
            )
        except Exception as e:
            print(e)



if __name__ == '__main__':
    worker()
while True:
    pass
