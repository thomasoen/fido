import uuid
import time
import sys
import urlparse
from boto.s3.connection import S3Connection
from boto.s3.key import Key

s3conn = S3Connection('AKIAILY2V2BWT5F5DNDA', 'Lr8DN9unBRg8xKA9BqFNpsGn+lvkdcc4bd69PSmH')
bucket = s3conn.get_bucket('crawler_cache')
 
#save_dir = "/home/ubuntu/webcache/"
#save_dir = "http://crawler_cache.s3-website-us-east-1.amazonaws.com/"
def persist_html(url, html):
    "saves HTML to a mounted s3 bucket"
    domain = urlparse.urlparse(url).hostname.lstrip("www.")
    fname = "{domain}_{timestamp}_{id}.html".format(domain=domain,
						    timestamp=int(time.time()),
						    id=str(uuid.uuid4()))

    try:
        html = html.encode('ascii', 'ignore')
        k  = Key(bucket)
	k.key = fname
	k.set_contents_from_string(html)
    except:
        print "ERROR WRITING FILE"

if __name__=="__main__":
    persist_html('http://www.test.com/something', sys.argv[1])
