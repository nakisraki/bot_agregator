###Mems - добавить softer архив и канал
###sms_message - добавить новые ежедневные
import re
from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup 
import os
import random
import urllib.request as ur
import codecs
import json
import io


###Ccылки на длинные youtube видео###
def yt_links(url):
    headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    ind = 0
    extract = []
    while (len(extract)!=5):
        try:
            searched=requests.get(url,headers=headers)
            soup=BeautifulSoup(searched.text,'html.parser')
            aid=soup.find('script',string=re.compile('ytInitialData'))
            extracted_josn_text=aid.text.split(';')[0].replace('window["ytInitialData"] =','').strip()
            video_results=json.loads(extracted_josn_text)
            item=video_results["contents"]['twoColumnBrowseResultsRenderer']['tabs'][1]["tabRenderer"]['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
            time = float(item[ind]['gridVideoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText'].replace(":","."))
            photo = item[ind]['gridVideoRenderer']['thumbnail']['thumbnails'][0]['url'].split("?")[0]
            video = "https://www.youtube.com/watch?v="+item[ind]['gridVideoRenderer']['videoId']
            title = item[ind]['gridVideoRenderer']['title']['runs'][0]['text']
            ind += 1
            if time<24:
                extract.append([title,photo,video,time])
        except:
            extract.append([0,0,0,0])
    return extract


                     #### NEWS ####

class news:
    def Ru_news():
      news_url="https://news.google.ru/news/rss"
      Client=urlopen(news_url)
      xml_page=Client.read()
      Client.close()
      soup_page=BeautifulSoup(xml_page,"xml")
      n=soup_page.findAll("item")
      news = []
      for i in range(len(n)):
          x = n[i].find("title").text.split('-')
          title,channel = x[0],x[1]+" Читать подробности"
          link = n[i].find("link").text
          news.append([title,channel,link])
      return news
    
                    #### HUMOR ####

class humor:
    def anecdot():
        head = ["https://4tob.ru/anekdots","https://nekdo.ru/","https://www.anekdot.ru/last/anekdot/","http://anekdotov.net/anekdot/today.html"]
        new , archive = [],[]
        for x in range(len(head)):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
            if x == 0:
                f = codecs.open("data/anekdot_archives.txt", "r", "utf-8")
                for line in f:
                    archive.append(line)
                f.close()  
            if x == 1:
                page = requests.get(head[x],headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                convert = soup.findAll("div",{"class":"text"})
                convert = [i.text for i in convert]
                new += convert
            if x == 2:
                page = requests.get(head[x],headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                convert = soup.findAll("div",{"class":"topicbox"})
                convert = [".".join(i.text.split('.')[:-1]) for i in convert if i.get("id")]
                new += convert
            if x == 3:
                page = requests.get(head[x],headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                convert = soup.findAll("div",{"class":"anekdot"})
                convert = [i.text for i in convert]
                new += convert
        new = [i for i in new if len(i)>5]
        archive = [i for i in archive if len(i)>5]
        return [new,archive]

    def fun_stories():
        new = []
        archive = []
        head = ["https://4tob.ru/stories/","http://anekdotov.net/story/today.html","https://surr.su/"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        for x in head:
            page = requests.get(x,headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            if x == head[0]:  
               f = codecs.open("data/fun_stories_arch.txt", "r", "utf-8")   
               for line in f: 
                  archive.append(line) if len(line)>10 else 'pass'
               f.close()   
            if x == head[1] :
               convert = soup.findAll("div",{"class":"anekdot"})
               convert = [i.text for i in convert]
               new += convert
            if x == head[2]:
               convert = soup.findAll("a")
               page = "https://surr.su/smeshnye_istorii.html?page=" + convert[3].text.split("№")[-1]
               page = requests.get(page,headers=headers) 
               soup = BeautifulSoup(page.content, 'html.parser')
               convert = soup.findAll("p",{"class":"for_br"})
               convert = [i.text for i in convert]
               new+=convert
        return [new,archive]

    def mems():
        ###udaff.com###
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        new,archive = [],[]
        archive = os.listdir("media/udaf")

        #index = 14361
        index = 2007 + len(archive)
        while index!=None:
            url = "https://udaff.com/view_listen/photo/page" + str(index) + ".html"
            r = requests.get(url).text
            soup = BeautifulSoup(r, 'html.parser')
            l = soup.find("div",{"class":"pic-cont"}).find("img").get("src")
            try:
                photo = "https://udaff.com" + l
                file = photo.split("/")[-1]
                if file not in archive and file not in new:
                    new.append(file)
                    ur.urlretrieve(photo, "media/udaf/" + file)
                    index += 1    
                else:
                    index=None
            except:
                index=None
        archive = os.listdir("media/udaf")
        new = sorted([int(i.split(".")[0]) for i in archive])[-20:]
        new = [str(i)+".jpg" for i in new if str(i)+".jpg" in archive]
        #try: 
           #urls = "https://pisez.com/2020/02/demotivatory-dnya-absolyutnye-hity.html"
           #full_page = requests.get(urls,headers=headers)
           #soup = BeautifulSoup(full_page.content, 'html.parser')
           #blocks = soup.find("div",{"class":"topic-full-content"})
           #a = str(blocks.find('img'))
           #b = a.split("<div style='clear:both;'></div>")
           #c = b[0].split("src=")
           #finish = [i.split(">")[0][1:-1] for i in c if "https" in i][:10]
           #for j in finish:
               #new.append(j)
        #except:
            #pass
        return [new,archive]

    def sms_message():
        new,archive = [],[]
        archive = os.listdir("media/sms_fun")
        return [news,archive]
  
    
    def afforisms():
        tag = ["\U0001F31E Цитаты дня","\U0001F46B Муж и Жен","\U0001F377 Алкоголь","\U0001F470 Брак","\U0001F475 Возраст","\U0001F937 Глупость"]
        new , archive = [],[]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        url = "https://www.anekdot.ru/release/aphorism/day/"
        full_page = requests.get(url,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        blocks = soup.findAll("div",{"class":"text"})
        texts = [i.text for i in blocks]
        new = texts
        with open('data/aphorisms.json', encoding='utf-8') as j:
            archive = json.load(j)
        return [new,archive,tag]
    
    
class tests:
    def geo_test():
        new,archive = [],[]
        with open('data/geo_test_data.json', encoding='utf-8') as j:
            archive = json.load(j)
        return [new,archive]
    def art_test():
        with open('data/paintings.json', encoding='utf-8') as j:
            archive = json.load(j)
        return archive

class adult:
    def short_stories():
        new,archive = [],[]
        with open('data/short_stories.json', encoding='utf-8') as j:
            archive = json.load(j)
        return  [new,archive]
    def comixes():
        new,archive = [],[]
        with open('data/a_comixes.json', encoding='utf-8') as j:
            archive = json.load(j)
        return  [new,archive]
    def long_stories():
        new,archive = [],[]
        with open('data/a_long_story.json', encoding='utf-8') as j:
            archive = json.load(j)
        return  [new,archive]
    def test():
        persons = os.listdir("media/xxx")
        persons = [i.split(".")[0] for i in persons]
        with open('data/persons_gallery.json', encoding='utf-8') as j:
            gallery = json.load(j)
        return  [persons,gallery]
        
        
class video_agr:
    def accidents():
        return os.listdir("media/temporary/Происшествия")
    def world():
        return os.listdir("media/temporary/Мир")
    def public():
        return os.listdir("media/temporary/Общество")
    def army():
        return [os.listdir("media/temporary/Армия"),os.listdir("media/weapon")]
    def science():
        with open('links.json', encoding='utf-8') as j:
            files = json.load(j)
        qwerty = [i for i in files["qwerty"]]
        pro_robots = [i for i in files["pro_robots"]]
        kosmo = [i for i in files["kosmo"]]
        techno = [i for i in files["techno"]]
        mad_science = [i for i in files["mad_science"]]
        lovi_moment = [i for i in files["lovi_moment"]]
        mn = [i for i in files["mn"]]
        videos = qwerty + pro_robots + kosmo + techno + mad_science + lovi_moment + mn
        random.shuffle(videos)
        return [os.listdir("media/temporary/Наука"),videos]
    def autos():
        return os.listdir("media/temporary/Авто")
    def fun():
        return [os.listdir("media/temporary/Развлечения"),os.listdir("media/fun_short_videos")]
    def movies():
        return os.listdir("media/temporary/movies")
    def web_cam():
        with open('web_cam.json', encoding='utf-8') as j:
            vids = json.load(j)
        return vids
        
        
        

