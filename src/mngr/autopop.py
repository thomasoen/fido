from bs4 import BeautifulSoup
import httplib2
import random, time, csv
import pprint as pp
import htmlhelper
import redis

def get_soup(url, delay=1):
    time.sleep(delay)
        
    try:
        h = httplib2.Http(".cache", timeout=4)
        resp, src = h.request(url, "GET")
        return BeautifulSoup(src)
    except:
        pp.pprint(resp)
        return BeautifulSoup("")

def get_merchants(soup):
    groups = soup.find("div", {"class":"top-merchants"})
    groups = groups.findAll("a")
    random.shuffle(groups)
    for m in groups:
        m_url = "http://www.bundle.com"+m["href"]
        yield m_url
        
def scrape_merchants(soup):
    merchants = soup.findAll("div", {"class":"feature-box"})[:-2]
    for m in merchants:
        if m.find("a"):
            fields = {}
            fields["url"] = "http://www.bundle.com"+m.find("a")["href"]
            fields["name"] = htmlhelper.unescape(m.find("a").getText())
            fields["html"] = m.prettify()
            for f in fields:
                fields[f] = fields[f].encode("ascii", "ignore")
            yield fields

red = redis.StrictRedis()

base = "http://www.bundle.com/merchant/listing/letter-{pg}/"

f = open("urlfiles/bundle_urls.csv", "wb")
w = csv.writer(f)

pages = list("0ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.shuffle(pages)

cntr = 0
for pg in pages[:1]:
    print "Starting "+pg
    pg_url = base.format(pg=pg)
    pg_soup = get_soup(pg_url)

    for group in get_merchants(pg_soup):
        group_soup = get_soup(group)
        
        for subgroup in get_merchants(group_soup):
            subgroup_soup = get_soup(subgroup)
            
            for merchant in scrape_merchants(subgroup_soup):
                w.writerow([group, subgroup]+merchant.values())
                if "url" in merchant:
                    red.sadd("urls_to_crawl", merchant['url'])
                cntr+=1
                if cntr%1000==0:
                    print "\tCollected {n} pages".format(n=cntr)
f.close()
raw_input("finished.")

