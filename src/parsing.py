from bs4 import BeautifulSoup
import re

def parse_html(html):
    data = {}
    try:
        soup = BeautifulSoup(html)
        for box in soup.findAll("div", {"class":re.compile("feature-box-section")}):

            if box.find("div", {"class":"hours"}):
                data['hours'] = {}
                for hour in box.find("div", {"class":"hours"}).findAll("li"):
                    hour = hour.getText('|').split('|')
                    data['hours'][hour[0].strip(":")] = hour[1]
                    
            if box.find("h3", text=re.compile("DAILY TRAFFIC")):
                data['traffic'] = {}
                for day in box.findAll("tr"):
                    daytraffic = day.find("div", {"class":"bar-fill"}).attrs['style']
                    daytext = day.text.strip().replace('\n\n\n\nLess traffic\nMore traffic', '')
                    data['traffic'][daytext] = daytraffic.split(":")[-1]

            if box.find("h3", text=re.compile("DEMOGRAPHICS")):
                data['demos'] = {}
                for demo in box.findAll("tr"):
                    name = demo.find("td")
                    value = demo.find("div", {"class":"bar-label"})
                    if value and name:
                        data['demos'][name.text] = value.text
                        
            if box.find("h3", text=re.compile("BUNDLE SCORE")):
                data['scores'] = {}
                for score in box.findAll("tr"):
                    name = score.find("td", {"class":"rating"})
                    value = score.find("td", {"class":"stat"})
                    if value and name:
                        name = name.text.strip()
                        if "POPULAR" in name:
                            name = "popularity"
                        elif "LOYALTY" in name:
                            name = "loyalty"
                        data['scores'][name] = value.text

        trans = soup.find(text=re.compile("[0-9] transactions"))
        if trans:
            data['transactions'] = trans.strip()

        tags = soup.find("div", {"id":"visible-tags"})
        if tags:
            data['tags'] = [label.text for label in soup.findAll("label")]

        for info in ['address', 'telephone', 'name']:
            value = soup.find("span", {"itemprop":info})
            if value:
                data[info] = value.text

        # Disabled due to:
        # Traceback (most recent call last):
        #   File "C:\Python27\lib\multiprocessing\queues.py", line 238, in _feed
        #     send(obj)
        # RuntimeError: maximum recursion depth exceeded while pickling an object

        # generalinfo = soup.find("div", {"class":"merchant-tab-unit bizinfo-tab-unit"})
        # if generalinfo:
        #     data['general'] = generalinfo
    except Exception, e:
        data['error'] = str(e)

    return data
