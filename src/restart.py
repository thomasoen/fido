from pymongo import Connection


db = Connection()['crawler']

cnt = db.bundle.count()-1
last_url = list(db.bundle.find().skip(cnt))
last_url = last_url[0]['url']

f = open('new_urls.txt', 'wb')

write = False
for line in open('all_urls.txt'):
  line = line.strip()
  if line == last_url:
    write = True
    continue

  if write==True:
    f.write(line + '\n')

f.close()
