import redis
import sys


def populate(url_file):
    r = redis.StrictRedis()

    for line in open(url_file):
        line = line.strip()
        r.rpush('urls_to_crawl', line)
        print "ADDING URL: %s" % str(line)


if __name__=="__main__":
    if len(sys.argv) > 1:
        f = sys.argv[1]
        populate(f)


