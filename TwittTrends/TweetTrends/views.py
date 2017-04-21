from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import json
from urllib.request import urlopen
from django.views.decorators.csrf import csrf_exempt
import boto3

global subscribed
# Create your views here.

keywords=['basketball, kobe, nowitzki, harden, westbrook, crossover, three pointer, free throw, warriors, rockets, nba',
          'electronics, camera, TV, computer, cell phone, kindle, audio, printer, DVD',
          'career, promotion, fire, hire, salary, wage, demotion',
          'music, composer, melody, rhythm, cello, bass, musician, sing, song, lyrics',
          'literature, dialogue, epigram, connotation, understatement, hyperbole, elegy',
          'science, physics, math, chemistry, biology, theory, principle, equation, research',
          'energy, oil, gas, new power, heat, fuel, solar, steam',
          'fitness, training, yoga, fat, muscle, nutrition, health',
          'winter, cold, christmas, freeze, frost, fireplace, hibernate',
          'fruit, apple, pear, watermelon, banana, blackberry, orange, lemon']



def Index(Request):
    return render(Request, 'TweetTrends/base.html')

def Post(Request):
    msg = Request.POST.get('Search', None)
    type = Request.POST.get('Type', None)
    print(msg)
    print(type)
    host = 'https://search-twitttrends-bfxt65yhs4orwjs5udape2p4tm.us-west-2.es.amazonaws.com/twitttrends/_search?size=10000&pretty=true&q='

    def search(url, term):
        uri = url + term
        response = requests.get(uri)
        results = json.loads(response.text)
        return results

    if (type == 'ddl'):
        if msg == 'Basketball':
            n = 0
        elif msg == 'Electronics':
            n = 1
        elif msg == 'Career':
            n = 2
        elif msg == 'Music':
            n = 3
        elif msg == 'Literature':
            n = 4
        elif msg == 'Science':
            n = 5
        elif msg == 'Energy':
            n = 6
        elif msg == 'Fitness':
            n = 7
        elif msg == 'Winter':
            n = 8
        elif msg == 'Fruit':
            n = 9
        r = search(host, keywords[n])
    elif (type == 'custom'):
        r = search(host, msg)

    user_name = {}
    cor = {}
    tweet = {}
    city = {}
    country = {}
    sentiment = {}
    length = int(r['hits']['total'])
    j = 0
    for res in r['hits']['hits']:
        user_name[j] = res['_source']['user_name']
        cor[j] = res['_source']['coordinates']
        tweet[j] = res['_source']['tweet']
        city[j] = res['_source']['city']
        country[j] = res['_source']['country']
        sentiment[j] = res['_source']['sentiment']
        j = j + 1
    hits = len(cor)
    length = {'hits': hits}
    coordinates = {}
    for i in range(hits):
        coordinates[i] = {'lat': cor[i]['lng'], 'lng': cor[i]['lat']}
    data = {'user_name': user_name, 'tweet': tweet, 'city': city, 'country': country,
            'coordinates': coordinates, 'length': length, 'sentiment': sentiment}

    return JsonResponse(data)

def polling(Request):
    msg = Request.GET.get('Search', None)
    type = Request.GET.get('Type', None)
    print(msg)

    host = 'https://search-twitttrends-bfxt65yhs4orwjs5udape2p4tm.us-west-2.es.amazonaws.com/twitttrends/_search?size=10000&pretty=true&q='

    def search(url, term):
        uri = url + term
        response = requests.get(uri)
        results = json.loads(response.text)
        return results

    if (type == 'ddl'):
        if msg == 'Basketball':
            n = 0
        elif msg == 'Electronics':
            n = 1
        elif msg == 'Career':
            n = 2
        elif msg == 'Music':
            n = 3
        elif msg == 'Literature':
            n = 4
        elif msg == 'Science':
            n = 5
        elif msg == 'Energy':
            n = 6
        elif msg == 'Fitness':
            n = 7
        elif msg == 'Winter':
            n = 8
        elif msg == 'Fruit':
            n = 9
        r = search(host, keywords[n])
    elif (type == 'custom'):
        r = search(host, msg)

    user_name = {}
    cor = {}
    tweet = {}
    city = {}
    country = {}
    sentiment = {}
    length = int(r['hits']['total'])
    print('new: ' + str(length))
    j = 0
    old_len = Request.GET.get('Num', None)
    print('old: ' + str(old_len))
    #old_len = int(old_len)
    j = 0
    for res in r['hits']['hits']:
        user_name[j] = res['_source']['user_name']
        cor[j] = res['_source']['coordinates']
        tweet[j] = res['_source']['tweet']
        city[j] = res['_source']['city']
        country[j] = res['_source']['country']
        sentiment[j] = res['_source']['sentiment']
        j = j + 1
    hits = len(cor)
    coordinates = {}
    for i in range(hits):
        coordinates[i] = {'lat': cor[i]['lng'], 'lng': cor[i]['lat']}
    data = {'user_name': user_name, 'tweet': tweet, 'city': city, 'country': country,
            'coordinates': coordinates, 'old_len': old_len, 'new_len': length, 'sentiment': sentiment}

    return JsonResponse(data)

@csrf_exempt
def snsrequest(request):
    context={"message":"Outside"}
    if request.method=="GET":
        return render(request,'TweetTrends/base.html')
    else:
        json_req = json.loads(request.body.decode("utf-8"))
        #rtype = request.headers['X-Amz-Sns-Message-Type']
        if json_req['Type'] == "SubscriptionConfirmation":
            topicArn = json_req['TopicArn']
            token = json_req['Token']
            url = json_req['SubscribeURL']
            urlopen(url).read()
            # snsclient = boto3.client('sns', region_name='us-west-2')
            # snsclient.confirm_subscription(TopicArn=topicArn, Token=token)
            # subscribed = True
        elif json_req['Type'] == "Notification":
            #print(json_req)
            message = json.loads(json_req["Message"])
            user_name = message.get('user_name')
            city = message.get('city')
            print('city ' + str(city))
            country = message.get('country')
            tweet = message.get('tweet')
            lat = message.get('lat')
            lng = message.get('lng')
            sentiment = message.get('sentiment')
            # coordinates=[lat,lng]

            e_data = {
                "user_name": user_name,
                "city": city,
                "country": country,
                "tweet": tweet,
                "coordinates": {"lat": lat, "lng": lng},
                "sentiment": sentiment
            }
            requests.post(
                'https://search-twitttrends-bfxt65yhs4orwjs5udape2p4tm.us-west-2.es.amazonaws.com/twitttrends/data',
                json=e_data)
            context = {"message": "I am in notification"}

    return render(request,'TweetTrends/base.html',context)