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
                    
            elif box.find("h2", text=re.compile("DAILY TRAFFIC")):
                data['traffic'] = {}
                for day in box.findAll("tr"):
                    daytraffic = day.find("div", {"class":"bar-fill"}).attrs['style']
                    daytext = day.text.strip().replace('\n\n\n\nLess traffic\nMore traffic', '')
                    data['traffic'][daytext] = daytraffic.split(":")[-1]

            elif box.find("h2", text=re.compile("DEMOGRAPHICS")):
                data['demos'] = {}
                for demo in box.findAll("tr"):
                    name = demo.find("td")
                    value = demo.find("div", {"class":"bar-label"})
                    if value and name:
                        data['demos'][name.text.replace("$", "")] = value.text

            elif box.find("h2", text=re.compile("TYPICAL COST")):
                desc = box.find("div", {"class":"description"})
                data['prices'] = desc.text.strip() if desc else None

                if data['prices']:
                    if len(re.findall("[$]\d+[-]\d+", data['prices'])) > 0:
                        data['price_range'] = re.findall("[$]\d+[-]\d+", data['prices'])[0]
                    if len(re.findall("total cost is [$]\d+", data['prices'])) > 0:
                        data['price_median'] = re.findall("total cost is ([$]\d+)", data['prices'])[0]

                        
            elif box.find("h2", text=re.compile("BUNDLE SCORE")):
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

            elif box.find("h2", text=re.compile("TOP .+ PLACES IN")):
                data['rankings'] = []
                for place in box.findAll("div", {"class":"row"}):
                    data['rankings'].append(str(place))

        trans = soup.find(text=re.compile("[0-9] transactions"))
        if trans:
            data['transactions'] = trans.strip()

        your_score = soup.find(text=re.compile("is rated ([0-9]+)"))
        if your_score:
            data['your_score'] = your_score.strip()
            if len(re.findall("rated (\d+)", your_score)) > 0:
                data['overall_score'] = re.findall("rated (\d+)", your_score)[0]

            if len(re.findall("#(\d+)", your_score)) > 0:
                data['area_ranking'] = re.findall("#(\d+)", your_score)[0]

        tags = soup.find("div", {"id":"visible-tags"})
        if tags:
            data['tags'] = [label.text for label in soup.findAll("label")]

        for info in ['address', 'telephone', 'name']:
            value = soup.find("span", {"itemprop":info})
            if value:
                data[info] = value.text

        
    except Exception, e:
        data['error'] = str(e)

    return data
