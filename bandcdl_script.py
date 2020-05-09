import urllib.request
from html.parser import HTMLParser
import re

class Parser(HTMLParser):
    text = "" 
    image_link = ""
    artist = ""
    mark_txt = True
    mark_artist = True
    mark_link = True
    in_art_id = False
    def handle_starttag(self, tag, attrs):
        if (not self.mark_link or not self.mark_txt or not self.mark_artist) and len(attrs) == 0:
            return
    
        if self.mark_link:
            if self.in_art_id!=True and tag == "div" and attrs[0][0] == "id" and attrs[0][1] == "tralbumArt":
                self.in_art_id = True
                return
            
            if self.in_art_id and tag == "a" and attrs[0][0] == "class" and attrs[0][1] == "popupImage":
                in_art_id = False
                for tmp in attrs[1:]:
                    if tmp[0] == "href":
                        self.image_link = tmp[1]
                        self.mark_link = False
                        return
        if self.mark_txt or self.mark_artist:
            if len(attrs) <= 1:
                return
            if tag == "meta":
                if self.mark_txt and attrs[0][0] == "name" and attrs[0][1] == "Description":
                    for tmp in attrs[1:]:
                        if tmp[0] == "content":
                            self.text = tmp[1]
                            self.mark_txt = False
                            return
                if self.mark_artist and attrs[0][0] == "property" and attrs[0][1] == "og:site_name":
                    for tmp in attrs[1:]:
                        if tmp[0] == "content":
                            self.artist = tmp[1]
                            self.mark_artist = False
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


urllib.request.urlretrieve(parser.image_link,save_path +
                                    "cover_" +
                                    re.sub(r'[\/:*?"<>|]+', '_', parser.artist+ "-" + re.search(r'album/.+', path).group(0)) + ".jpg")

for i in range(0, len(album_list)):
    print("downloading {0}...".format(album_list[i]))
    urllib.request.urlretrieve(links[i], save_path+re.sub(r'[\/:*?"<>|]+', '_',parser.artist+" - "+album_list[i])+".mp3")

print("Done")

