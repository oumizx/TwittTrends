# TwittTrends

Author : Haonan Zhu(hz1396), Lu Liu(ll3346)

E-mail : [hz1396@nyu.edu](mailto:hz1396@nyu.edu), [ll3346@nyu.edu](mailto:ll3346@nyu.edu)

URL: http://twitttrends-env.52mg4u6s2j.us-west-2.elasticbeanstalk.com/

Release: https://github.com/oumizx/TwittTrends/releases/tag/1.0.0

### Overview

We realize to show the tweets indexed in real time and total number of a specific keyword in real time. When click the marker, we can get the user and content of the tweet, the position and sentiment are also visible.

**Back End**

Based on Django framework. We fetch Tweet data through Twitter Streaming API, index and store it on ElasticSearch. We use AWS SQS service to create a processing queue for Tweets, adding the tweets to SQS. Then we create AWS SNS service to update the status on each tweet.

We define a worker pool to pick up message from queue to process. When a tweet is processing, send a notification through AWS SNS to HTTP endpoint.

We also realize event queue with Kafka.

**Front End**

We can see new markers’ drop effects automatically on the map when a new tweet is indexed. User can either choose one keyword or type in a specific word to search qualified tweets. Sentiment is realized through Alchemy API. We also realize real time appearance through long polling. 

**Deployment**

The whole application is deployed on AWS Elastic Beanstalk.

![alt tag](https://github.com/oumizx/TwittTrends/blob/master/screenshot.png)
