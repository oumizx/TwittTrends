import time
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import boto3
import json

sqs = boto3.resource('sqs')
sns = boto3.client('sns', region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName='twitttrends-17')
arn = 'arn:aws:sns:us-west-2:661110844100:Tweet_topic_notification'


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


def worker(queue):
    while True:
        for message in queue.receive_messages(MessageAttributeNames=['All']):

            if message.message_attributes is not None:
                tweet = message.body
                user_name = message.message_attributes.get('User_name').get('StringValue')
                city = message.message_attributes.get('City').get('StringValue')
                country = message.message_attributes.get('Country').get('StringValue')
                lat = message.message_attributes.get('Latitude').get('StringValue')
                lng = message.message_attributes.get('Longitude').get('StringValue')

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

            message.delete()


if __name__ == '__main__':
    worker(queue)
while True:
    pass
