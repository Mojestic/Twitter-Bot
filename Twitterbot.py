import tweepy
import time



def getAPI(api_keys, access_tokens):
    try:
        auth = tweepy.OAuthHandler(api_keys[0], api_keys[1])
        auth.set_access_token(access_tokens[0], access_tokens[1])
    except IndexError as err:
        print('api_keys and access_tokens each require two elements')
        raise err
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api



def userQueryTweetMax(need_query=False):
    max_tweets, query = None, None
    while True:
        try:
            max_tweets = int(input('Max tweets to find: '))
            if max_tweets < 1:
                print('Need a positive integer')
                continue
            if need_query:
                query = input('Provide search query: ')
            break
        except ValueError:
            print('Need a positive integer')
    if query:
        return max_tweets, query
    else:
        return max_tweets



def userReqs():
    reqs = {
        'follows': -1,
        'statuses': -1
    }
    for req in reqs.keys():
        while True:
            try:
                reqs[req] = int(
                    input(f'Requisite {req} for follow back (0 for none): '))
                break
            except ValueError:
                print('Need an integer')
    return reqs



def checkReqs(follower, reqs):
    return follower.followers_count >= reqs['follows'] and follower.statuses_count >= reqs['statuses']



def followBack(api):
    reqs = userReqs()
    for follower in tweepy.Cursor(api.followers).items():
        if checkReqs(follower, reqs) and not follower.following:
            follower.follow()
            print(f'Followed {follower.name}')
            

def likeRetweet(api, user_lang="en"):
    max_tweets, query = userQueryTweetMax(True)
    for tweet in tweepy.Cursor(api.search, query, lang=user_lang).items(max_tweets):
        try:
            if not tweet.favorited:
                tweet.favorite()
            if not tweet.retweeted:
                tweet.retweet()
                print(
                    f'Liked and retweeted "{tweet.text}" from {tweet.user.screen_name}')
        except tweepy.TweepError as err:
            print(
                f'Tweet "{tweet.text}" not liked and retweeted: {err.reason}')
        except StopIteration:
            break
        

