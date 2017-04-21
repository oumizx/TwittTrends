from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import boto3
import json

sqs = boto3.resource('sqs')
sns = boto3.client('sns')
queue = sqs.get_queue_by_name(QueueName='twitttrends-17')
arn = 'arn:aws:sqs:us-west-2:661110844100:twitttrends-17'


def worker(queue):
    for message in queue.receive_messages(MessageAttributeNames=['All'], VisibilityTimeout=30, MaxNumberOfMessages=1):
        message.delete()
        print('deleted')
    print('delete complete')
    return True


if __name__ == '__main__':
    worker(queue)
while True:
    pass
