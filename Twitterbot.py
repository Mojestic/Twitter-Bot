import tweepy


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
