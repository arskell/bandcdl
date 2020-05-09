import urllib.request
from html.parser import HTMLParser
import re

class Parser(HTMLParser):
    text = "" 
    mark = True
    def handle_starttag(self, tag, attrs):
        if self.mark:
            if len(attrs) <= 1:
                return
            if tag == "meta" and attrs[0][0] == "name" and attrs[0][1] ==  "Description":
                for tmp in attrs[1:]:
                    if tmp[0] == "content":
                        self.text = tmp[1]
                        self.mark = False
                        return

    
print("Enter url path to the album: ")
path = input()

raw_html = urllib.request.urlopen(path)

parser = Parser()
data = raw_html.read().decode("utf-8")
parser.feed(data)

parser.text = re.sub('&#39;', "'", parser.text)
parser.text = re.sub('&quot;', '"', parser.text)

album_list_txt = re.findall(r'\d+[.][ ].+\n', parser.text)

links = re.findall(r'https://t4.bcbits.com/stream/[^"]+', data)

album_list = []
for e in album_list_txt:
    album_list.append(re.search(r'[ ].+', e).group(0)[1:])

if len(album_list) != len(links):
    raise("Parsing error")

print("found {0} tracks".format(len(album_list)))
print("Enter save directory:")

save_path = input()
if save_path[-1]!='/':
    save_path+='/'

for i in range(0, len(album_list)):
    print("downloading {0}...".format(album_list[i]))
    urllib.request.urlretrieve(links[i], save_path+re.sub(r'[\/:*?"<>|]+', '_', album_list[i])+".mp3")

print("Done")


