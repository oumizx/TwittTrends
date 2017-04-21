# TwittTrends

Author : Haonan Zhu(hz1396), Lu Liu(ll3346)

E-mail : [hz1396@nyu.edu](mailto:hz1396@nyu.edu), [ll3346@nyu.edu](mailto:ll3346@nyu.edu)

URL: http://twitttrends-env.52mg4u6s2j.us-west-2.elasticbeanstalk.com/

Release: https://github.com/oumizx/TwittTrends/releases/tag/1.0.0

### Overview

**Streaming**

- Reads a stream of tweets from the Twitter Streaming API. 
- After fetching a new tweet, check to see if it has geolocation info and is in English.
- Once the tweet validates these filters, send a message to SQS for asynchronous processing on the text of the tweet

**Worker**

- Define a worker pool that will pick up messages from the queue to process. These workers should each run on a separate pool thread.
- Make a call to the sentiment API using Alchemy. This can return a positive, negative or neutral sentiment evaluation for the text of the submitted Tweet.
- As soon as the tweet is processed send a notification using SNS to an HTTP endpoint that contains the information about the tweet.

**Kafka**

- We implement Kafka as event queue.

**Backend**

- We use Django as framework.


- On receiving the notification, index this tweet in Elasticsearch. 
- The backend should provide the functionality to the user to search for tweets that match a particular keyword. 

**Frontend**

- When a new tweet is indexed, we will see the drop effects.
- User can search their index via a free text input or a dropdown.
- Qualified tweets are plotted on the map. 
- Use Alchemy API to indicate the sentiment. Alternatively, you can come up with any other style to represent the sentiment of the tweet.?

**Deployment**

- Deploy application on AWS Elastic Beanstalk.

![alt tag](https://github.com/oumizx/TwittTrends/blob/master/screenshot.png)
