import uuid
import time
import sys
import urlparse

save_dir = "/home/ubuntu/webcache/"

def persist_html(url, html):
    "saves HTML to a mounted s3 bucket"
    domain = urlparse.urlparse(url).hostname.lstrip("www.")
    fname = "{domain}_{timestamp}_{id}.html".format(domain=domain,
						    timestamp=int(time.time()),
						    id=str(uuid.uuid4()))

    f = open(save_dir + fname, 'wb')
    try:
        html = html.encode('ascii', 'ignore')
        f.write(html)
    except:
        print "ERROR WRITING FILE"
    f.close()


if __name__=="__main__":
    persist_html('test.com', sys.argv[1])
