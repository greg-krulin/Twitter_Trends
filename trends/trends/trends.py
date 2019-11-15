"""Visualizing Twitter Sentiment Across America
Project Finished by Gregory Krulin and Uzzi Valencia"""

from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait
from string import ascii_letters
from ucb import main, trace, interact, log_current_line



###################################
# Phase 1: The Feelings in Tweets #
###################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    if type(tweet['text']) == str:
            return tweet['text']
    else:
        print('Error: text must be a string')
    

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    if (type(tweet['time']) == datetime) or (type(tweet['time'])==None):
        return tweet['time']
    
    else:
        print('Error: datetime must be class datetime.datetime')
    

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    if (type(tweet['latitude']) == float or type(tweet['latitude']) == int) and (type(tweet['longitude']) == float or type(tweet['longitude']) == int):
        return make_position(tweet['latitude'], tweet['longitude'])
    else:
        print('Error: lat & lon must be type float')
# The tweet abstract data type, implemented as a function.

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> latitude(tweet_location_fn(t))
    38
    """
    "*** YOUR CODE HERE ***"
    assert type(text) is str, 'ERROR! text must be str object'
    #if type(time) != type(None): 
     #   assert type(time) is datetime  ,'ERROR! time must be datetime object'
    #if type(lat) != type(None):
      #  assert type(lat) is float or type(lat) is int , 'ERROR! lat must be float or int object'
    #if type(lon) != type(None):
    #    assert type(lon) is float or type(lon) is int, 'ERROR! lon must be floa or intt object'
    #dic = {'text': text,'time': time, 'latitude': lat, 'longitude': lon}
    lst = [text,time,lat,lon]
    def fn_tweet(cmnd):
        nonlocal lst
        if cmnd == 'text':
            return lst[0]
        if cmnd == 'time':
            return lst[1]
        if cmnd == 'lat':
            return lst[2]
        if cmnd == 'lon':
            return lst[3]
        else: print("error: function needs an appropriate command")
    return fn_tweet
    # Please don't call make_tweet in your solution

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_words(tweet):
    """Return the words in a tweet."""
    if type(tweet)== type(lambda x: x):
        return extract_words(tweet_text_fn(tweet))
    else:
        return extract_words(tweet_text(tweet))

def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    lst = []
    for i in text:
        if i in ascii_letters:
            lst += i
        else:
            lst+= ' '
    lst = ''.join(lst)
    return lst.split()

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    "*** YOUR CODE HERE ***"
    return value

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    return type(s) == float or type(s) == int

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return s

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    # You may change any of the lines below.
    average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    
    words = tweet_words(tweet)
    storage = 0
    count = 0
    for i in words:
        
        s = get_word_sentiment(i)
        
        if has_sentiment(s):
           storage = storage+sentiment_value(s)
           count +=1
        else:
            pass
        
        
    if count>0:
        average = make_sentiment(storage/count)
        return average
    else:
        return make_sentiment(None)


#################################
# Phase 2: The Geometry of Maps #
#################################

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> round5 = lambda x: round(x, 5) # Rounds floats to 5 digits
    >>> tuple(map(round5, find_centroid(triangle)))
    (3.0, 2.0, 6.0)
    >>> tuple(map(round5, find_centroid([p1, p3, p2, p1])))
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    (1.0, 2.0, 0.0)
    """
    "*** YOUR CODE HERE ***"
    area = 0
    i = 0
    c_x = 0
    c_y = 0
    
    while i < (len(polygon) - 1):
        area += (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i]))
        i= 1 + i
        
    area = 1/2*(area)
    if area == 0:
        return latitude(polygon[0]), longitude(polygon[0]), 0
    
    else:
        i = 0
        while i < (len(polygon) - 1):
            c_x +=  (latitude(polygon[i])+latitude(polygon[i+1]))*((latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i])))
            c_y += (longitude(polygon[i])+longitude(polygon[i+1]))*((latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i])))
            i +=1
    
        c_x = ((1/(6*area)))*c_x
        c_y = ((1/(6*area)))*c_y
        return c_x, c_y, abs(area)


def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    "*** YOUR CODE HERE ***"
    c_x = 0
    c_y = 0
    area = 0
    j = 0
    centroids = []
    
    for poly in polygons:
        centroids.append(find_centroid(poly))
    
    while j < len(centroids):
        area+=centroids[j][2]
        c_x += centroids[j][0]* centroids[j][2]
        c_y += centroids[j][1]* centroids[j][2]
        j+=1
    
    return make_position(c_x/area, c_y/area)
        

    


###################################
# Phase 3: The Mood of the Nation #
###################################

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    tweets_by_state = {}
    "*** YOUR CODE HERE ***"
            
    for t in tweets:
        if type(t)==type( lambda x: x):
            loc = tweet_location_fn(t)
        else:
            loc = tweet_location(t)
        minstate = ['CA',10000000]
        for state in us_states:
            statecenter = find_state_center(us_states[state])
            if geo_distance(statecenter,loc)<minstate[1]:
                minstate[0] = state
                minstate[1] = geo_distance(statecenter,loc)
        if minstate[0] in tweets_by_state:
                tweets_by_state[minstate[0]].append(t)
        else:
            tweets_by_state[minstate[0]] = [t]
    
    return tweets_by_state

def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    #analyze_tweet_sentiment()
    for state in tweets_by_state:
        tweets = tweets_by_state[state]
        average = 0
        count = 0
        for t in tweets:
            s = analyze_tweet_sentiment(t)
            if has_sentiment(s):
                average = average + (sentiment_value(s))
                count+=1
        if count > 0:
            averaged_state_sentiments[state] = sentiment_value(make_sentiment((average)/count))
            
    return averaged_state_sentiments



##########################
# Command Line Interface #
##########################

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_state_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_query(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', action='store_true')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))
