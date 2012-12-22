import redis


PROXY_USER = ''
PROXY_PASSWORD = ''
PROXIES = []


def round_robin(list):
    while True:
        for item in list:
            yield(item)

def generate_urls_from_file(urlsFile):
    proxies = round_robin(PROXIES)
    for line in open(urlsFile):
        proxy = 'http://%(username)s:%(pass)s@%(ip)s:%(port)d/' % \
            {'username': PROXY_USER, 'pass': PROXY_PASSWORD, 
                'ip': proxies.next(), 'port': 55555}
        yield (line.strip('\n'), proxy)
    raise StopIteration()

def generate_urls_from_db():
    proxies = round_robin(PROXIES)
    red = redis.StrictRedis()
    while red.srandmember('urls_to_crawl'):
        proxy = 'http://%(username)s:%(pass)s@%(ip)s:%(port)d/' % \
            {'username': PROXY_USER, 'pass': PROXY_PASSWORD, 
                'ip': proxies.next(), 'port': 55555}
        #grab the next url
        nextUrl = red.spop('urls_to_crawl')
        yield (nextUrl, proxy)
    raise StopIteration()

