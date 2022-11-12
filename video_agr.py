## -*- coding: utf-8 -*-
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
import ffmpy
import time
import shutil
import youtube_dl
import urllib.request as ur
from selenium import webdriver
import urllib.parse
import yadisk
from selenium.webdriver.common.keys import Keys
import pyautogui
from pathlib import Path
import sqlite3
import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

def delete_files(x):
    for i in os.listdir(x):  
        if i.startswith("unname") == False:
            print("Remove file " + i)
            os.remove(x+ "/" +i)

def full_delete_files(x):
    for i in os.listdir(x):
        print("Remove file " + i)
        try:
            os.remove(x+ "/" +i)
        except:
            shutil.rmtree(x+ "/" +i, ignore_errors=True)

def check_video_folder(x):
    for i in os.listdir(x):
        size = Path(x+ "/" +i).stat().st_size/1048000
        if size>50 or size==0:
            print("Remove file " + i)
            try:
                os.remove(x+ "/" +i)
            except:
                shutil.rmtree(x+ "/" +i, ignore_errors=True)

                


def django_remove():
    db = sqlite3.connect('/home/kir/Загрузки/aiogram/aiogram/app/db.sqlite3')
    c = db.cursor()
    c.execute('DELETE FROM editapp_files')
    db.commit()
    db.close()
    head = "C:/Users/Администратор/Desktop/django/editor/editorapp/media/aio/"
    folders = os.listdir(head)
    for fold in folders:
        files = os.listdir(head+fold)
        for file in files:
            path = head + fold + "/" + file
            try:
                os.remove(path)
            except:
                print(path)
    

def django_import():
    db = sqlite3.connect('C:/Users/Администратор/Desktop/django/editor/editorapp/db.sqlite3')
    c = db.cursor()
    f = "/home/kir/Загрузки/aiogram/aiogram/app/media/temporary/"
    folders = os.listdir(f)
    tags = {"Армия":3,"Авто":4,"Интернет":5,"Мир":6,"Наука":7,"Общество":8,"Происшествия":9,"Развлечения":10,"Спорт":11,"Стиль":12,"movies":13,"Экономика":14,"web":15,"Игры":16}
    #count = len(c.execute("SELECT * FROM `editapp_files`").fetchall()) + 1000
    count = 1300
    for fold in folders:
        if fold in tags:
            files = os.listdir(f+fold)
            check = c.execute("SELECT video FROM editapp_files WHERE `category_id` = ?", (tags[fold],)).fetchall()
            check = [i[0].split("/")[-1] for i in check]
            for file in files:
                if file not in check:
                    count += 1
                    name = ''
                    if file.startswith('unname'):
                        name = file.split(".mp")[0].replace("unname","")
                    else:
                        name = file.split(".mp")[0]
                        description = 'none'
                    name = name.replace("+"," ").replace("  "," ").replace("#"," ")
                    image = '0'
                    draft = True
                    url = str(count)
                    published_by = datetime.datetime.now()
                    video = "aio/" + fold + "/" + file
                    category = tags[fold]
                    path = "media/temporary/" + fold + "/" + file
                    dist = "C:/Users/Администратор/Desktop/django/editor/editorapp/media/aio/" + fold + "/"
                    shutil.copy(path,dist)
                    if file in os.listdir(dist):
                        try:
                            c.execute("INSERT INTO 'editapp_files' ('name','description','image','url','draft','published_by','category_id','video') VALUES(?,?,?,?,?,?,?,?)",(name,description,image,url,draft,published_by,category,video))
                        except:
                            count+=1
                    else:
                        print("not file in dict")
    links = "C:/Users/Администратор/Desktop/aiogram/app/media/links/science/"
    files = [i for i in os.listdir(links) if i.endswith(".mp4")]
    for file in files:
        check = c.execute("SELECT video FROM editapp_files WHERE `category_id` = ?", (7,))
        check = [i[0].split("/")[-1] for i in check]
        if file not in check:
            count += 1
            name = file.split(".mp")[0].replace("+"," ").replace("  "," ").replace("#"," ")
            description = 'none'
            image = '0'
            draft = True
            url = str(count)
            published_by = datetime.datetime.now()
            video = 'aio/' + "Наука" + '/' + file
            category = 7
            path = "media/links/science/" + file
            dist = "C:/Users/Администратор/Desktop/django/editor/editorapp/media/aio/" + "Наука" + "/"
            shutil.copy(path,dist)
            c.execute("INSERT INTO 'editapp_files' ('name','description','image','url','draft','published_by','category_id','video') VALUES(?,?,?,?,?,?,?,?)",(name,description,image,url,draft,published_by,category,video))
    
    db.commit()
    db.close()  


    
    
class video: 
    def izvestia():
        head = "https://iz.ru"
        html = "https://iz.ru/video"
        full_page = requests.get(html,headers=headers)
        print(full_page)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        blocks = soup.findAll("a")
        blocks = [head + i.get("href") for i in blocks if i.get("href") and "video" in i.get("href")]
        print(blocks)
        pages = blocks[1:]
        videos = {}
        for i in pages:
            try:
                full_page = requests.get(i,headers=headers)
                soup = BeautifulSoup(full_page.content, 'html.parser')
                tag = soup.find("div",{"class":"rubrics_btn"}).text
                vid = head + soup.find("iframe").get("src").split("#")[0]
                tag = tag.replace("\n","")
                if tag not in videos:
                    videos[tag] = []
                videos[tag].append(vid)
            except:
                pass
        for j in videos:
            if not os.path.isdir("media/temporary/" + j):
                os.mkdir("media/temporary/" + j)
            path = "media/temporary/" + j + "/"
            vids = videos[j]
            for k in vids:
                try:
                    full_page = requests.get(k,headers=headers)
                    soup = BeautifulSoup(full_page.content, 'html.parser')
                    title = soup.find("title").text + ".mp4"
                    title = title.replace(",", " ")
                    ydl_opts = {'outtmpl': path+title}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([k])
                    time.sleep(3)
                except:
                    pass
    def y_pl():
        new = []
        path = ""
        #pages = ["https://www.yapfiles.ru/cat/1/rating_by_pop/period/1/page/1/","https://www.yapfiles.ru/cat/1/rating_by_rank/period/1/page/1/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/2/page/1/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/3/page/1/"]
        #pages = ["https://www.yapfiles.ru/cat/1/rating_by_rank/period/1/page/1/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/2/page/1/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/3/page/1/"]
        pages = ["https://www.yapfiles.ru/cat/1/rating_by_pop/period/1/page/1/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/1/page/2/","https://www.yapfiles.ru/cat/1/rating_by_pop/period/1/page/3/","https://www.yapfiles.ru/cat/1/rating_by_com/period/1/page/1/","https://www.yapfiles.ru/cat/1/rating_by_com/period/1/page/2/","https://www.yapfiles.ru/cat/1/rating_by_com/period/1/page/3/","https://www.yapfiles.ru/cat/1/sort_by_new/page/1/","https://www.yapfiles.ru/cat/1/sort_by_new/page/2/","https://www.yapfiles.ru/cat/1/sort_by_new/page/3/"]
        for html in pages:
            full_page = requests.get(html,headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            blocks = soup.findAll("a",{"class":"single"})
            video = [i.get("href")+"?hq=1" for i in blocks if i.get("href")]
            for i in video :
                try:
                    html = i
                    full_page = requests.get(html,headers=headers)
                    soup = BeautifulSoup(full_page.content, 'html.parser')
                    block = soup.find("input",{"name":"direct_link"}).get("value")
                    info = soup.find("h2").text.replace("\n","")
                    name = block.split("?")[1] + ".mp4"
                    tok = soup.find("h1").text
                    accidents = ["Аварии/Катастрофы","Жесть",]
                    if info in accidents:
                        path = "media/temporary/Происшествия/"
                        name = "unname" + tok + ".mp4"
                    elif info == "Авто/Мото":
                        path = "media/temporary/Авто/"
                        name = "unname" + tok + ".mp4"
                    elif info == "Новости/Политика":
                        path = "media/temporary/Общество/"
                        name = "unname" + tok + ".mp4"
                    else:
                        name = "unname" + tok + ".mp4"
                        path = "media/temporary/Развлечения/"
                        new.append(path+name)
                    name = name.replace(","," ")    
                    exist = os.listdir(path)
                    if name not in exist:
                        print(block)
                        r  = requests.get(block)
                        with open(path+name, 'wb') as f:
                            print(path+name)
                            f.write(r.content)
                except:
                    pass

        return True        

    def press_fun():
        path = "media/temporary/Развлечения/"
        http = "https://pressa.tv/video/"
        page = requests.get(http,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        convert = soup.findAll("video")
        src = "https://pressa.tv"
        links = [src+i.find("source").get("src") if i.find("source").get("src") else src + i.find("source").get("data-src") for i in convert]
        for i in links:
            video = i
            file = video.split("/")[-1]
            file = file.replace(","," ")
            if file not in os.listdir(path):
                 try:
                     dat = ur.urlopen(video)
                     if int(dat.info()["Content-Length"])<8850000:
                         ur.urlretrieve(video,path+file)
                 except:
                     dat = ur.urlopen(video)
                     if int(dat.info()["Content-Length"])<8850000:   
                       r  = requests.get(path)
                       with open(path + file, 'wb') as f:
                           print(path_file)
                           f.write(r.content)
        return True        

class youtube:
    def loads(channels,folder):
        new = []
        exist = os.listdir("media/temporary/" + folder)
        for x in channels:
            driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
            URL = x
            driver.get(URL)
            time.sleep(5)
            html = driver.page_source
            page = "https://www.youtube.com"
            soup = BeautifulSoup(html, "html.parser")
            videos = soup.find_all("a",{"class":"yt-simple-endpoint style-scope ytd-video-renderer"})
            vid = [[i.get("title"),page+i.get("href")] for i in videos if i.get("href")]
            if folder == "Спорт":
                vid = vid[:12]
            if folder == "Наука":
                vid = vid[:6]
            path = "media/temporary/" + folder + "/"
            #path  = "media/fun_short_videos/"
            for j in vid:
                name = j[0].replace(","," ") + ".mp4"
                new.append(name)
                if name not in exist and "Анонс" not in name:
                    ydl_opts = {'outtmpl': path+name,"format":"18"}
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                           ydl.download([j[1]])
                    except:
                        pass       
            driver.close()
            time.sleep(1)
        allow = ["Происшествия","Армия","Авто"]
        if folder in allow:
            for i in exist:
                if i not in new and i.startswith("unname")==False:
                    os.remove(path+i)
        exist = os.listdir("media/temporary/" + folder)
        for i in exist:
            if i.endswith(".mp4") == False:
                try:
                    os.remove(path+i)
                except:
                    shutil.rmtree(path+i,ignore_errors=True)
        return True

    def archive(channels,folder):
        new = []
        exist = os.listdir("media/" + folder)
        driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
        URL = channels
        driver.get(URL)
        time.sleep(10)
        html = driver.page_source
        page = "https://www.youtube.com"
        soup = BeautifulSoup(html, "html.parser")
        videos = soup.find_all("a",{"class":"yt-simple-endpoint style-scope ytd-grid-video-renderer"})
        vid = [[i.get("title"),page+i.get("href")] for i in videos if i.get("href")]
        print(vid)
        path = "media/" + folder + "/"
        for j in vid:
            name = j[0].replace(","," ") + ".mp4"
            new.append(name)
            if name not in exist:
                ydl_opts = {'outtmpl': path+name,"format":"18"}
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([j[1]])
                except:
                    pass       
        driver.close()
        return True 
    

class youtube_links:
    def links(url,channels,folder,total):
        new = []
        page = "https://www.youtube.com"
        if channels!="temporary":
            exist = os.listdir("media/links/" + folder)
        else:
            exist = os.listdir("media/temporary/" + folder)
        driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
        URL = url
        driver.get(URL)
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        videos = soup.find_all("ytd-grid-video-renderer")[:10]
        cont = [[i.find("img").get("src").split("?")[0],i.find("a",{"id":"video-title"}).get("title").replace(" ","+").replace(",","_"),page+i.find("a",{"id":"video-title"}).get("href")] for i in videos if i.find("img").get("src") and i.find("a",{"id":"video-title"}).get("title") and i.find("a",{"id":"video-title"}).get("href")]
        driver.close()
        for j in cont[:total]:
            name_video = re.sub(r'[^A-zА-я0-9+_]', '', j[1]) + ".mp4"
            name_img = re.sub(r'[^A-zА-я0-9+_]', '', j[1]) + ".jpg"
            path_video = urllib.parse.quote(name_video) 
            path_img = urllib.parse.quote(name_img) 
            if name_video not in exist:
                if channels == "temporary":
                    path = "media/temporary/" + folder + "/"
                else:
                    path = "media/links/" + folder + "/"
                #ydl_opts = {'outtmpl': path+name_video,"format":"22"}
                try:
                    with youtube_dl.YoutubeDL() as ydl:
                        info_dict = ydl.extract_info(j[2], download=False)
                    dur = int(info_dict["duration"])
                    print(dur)
                    time.sleep(5)
                    if dur<1000:
                        ydl_opts = {'outtmpl': path+name_video,"format":"18"}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([j[2]])
                        time.sleep(5)
                        r  = requests.get(j[0])
                        with open(path + name_img, 'wb') as f:
                            f.write(r.content)
                        new.append(path_video)    
                        
                except:
                    print(path + name_img)
        if channels != "temporary":
            with open('links.json', encoding='utf-8') as j:
                data = json.load(j)   
            data[channels] = new
            with open('links.json', 'w') as outfile: json.dump(data, outfile)

    def movie_thrailers(url):
        new = []
        page = "https://www.youtube.com"
        exist = os.listdir("media/temporary/movies")
        driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
        URL = url
        driver.get(URL)
        #driver.execute_script("window.scrollTo(0, 12040)")
        SCROLL_PAUSE_TIME = 2.0
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                 break
            last_height = new_height
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        videos = soup.find_all("ytd-grid-video-renderer")
        print("Видео всего:"+ str(len(videos)))
        random.shuffle(videos)
        videos = videos[:25]
        cont = [[i.find("img").get("src").split("?")[0],i.find("a",{"id":"video-title"}).get("title").replace(" ","+").replace(",","_"),page+i.find("a",{"id":"video-title"}).get("href")] for i in videos if i.find("img").get("src") and i.find("a",{"id":"video-title"}).get("title") and i.find("a",{"id":"video-title"}).get("href")]
        driver.close()
        for j in cont:
            name_video = re.sub(r'[^A-zА-я0-9+_]', '', j[1]) + ".mp4"
            name_img = re.sub(r'[^A-zА-я0-9+_]', '', j[1]) + ".jpg"
            path_video = urllib.parse.quote(name_video) 
            path_img = urllib.parse.quote(name_img) 
            if name_video not in exist:
                path = "media/temporary/movies/"
                try:
                    with youtube_dl.YoutubeDL() as ydl:
                        info_dict = ydl.extract_info(j[2], download=False)
                    dur = int(info_dict["duration"])
                    print(dur)
                    time.sleep(5)
                    if dur<1000:
                        ydl_opts = {'outtmpl': path+name_video,"format":"18"}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([j[2]])
                        time.sleep(3)
                except:
                    print(path + name_img)
        return 0


class web_cam:

    def light():
        head = "https://www.erosberry.com"
        vids = {}
        count = 0
        while len(vids)<10:
            print(len(vids))
            a = random.randint(97,122)
            html = "https://www.erosberry.com/models?order=rate&letter=" + chr(a)
            full_page = requests.get(html,headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            blocks = soup.findAll("a",{"class":"item-post"})
            blocks = [i.get("href") for i in blocks if i.get("href")]
            try:
                page = random.choice(blocks)
                html = head + page   
                full_page = requests.get(html,headers=headers)
                soup = BeautifulSoup(full_page.content, 'html.parser')
                blocks = soup.findAll("a",{"class":"item-post"})
                videos = [ i for i in blocks if i.get("href") and "videos" in i.get("href")]
                print("length is " + str(len(videos)))
                if len(videos)>0:
                    try:
                        tag = random.choice(videos)
                        vid = "https://www.erosberry.com" + tag.get("href")
                        name = tag.find("img").get("alt").split("/")[-1]
                        image = tag.find("img").get("src")
                        if "https:" not in image:
                            image = "https:"+image
                        full_page = requests.get(vid,headers=headers)
                        soup = BeautifulSoup(full_page.content, 'html.parser')
                        vid = soup.find("source").get("src")
                        if "http" not in vid:
                            vid = "https:"+vid
                        response = requests.get(vid).status_code
                        if response == 200 and name not in vids:
                            
                            r  = requests.get(image)
                            with open("media/temporary/web/" + name + ".jpg", 'wb') as f:
                                f.write(r.content)
                        
                            vids[name] = ["media/temporary/web/" + name + ".jpg",vid]
                        else:
                            print(response)
                    except:
                        pass
            except:
                pass
        data = {}
        print(vids)
        with open('web_cam.json', encoding='utf-8') as j:
            data = json.load(j)
        print(data)
        data = vids
        with open('web_cam.json', 'w') as outfile: json.dump(data, outfile)
        return True

    def medium(x):
        html = x
        full_page = requests.get(html,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        blocks = soup.findAll("a")
        block = [i.get("href") for i in blocks if i.get("href") and i.get("href").startswith("http") and 'google' not in i.get("href")]
        count = 1
        urls = []
        for i in block:
            driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
            driver.get(i)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            driver.close()
            try:
                videos = soup.find("script",{"type":"application/ld+json"}).text
                y = json.loads(videos)
                vid = y['contentUrl'].replace("720","240")
                length = soup.find("span",{"class":"i-length"})
                leng = int(length.text.split(":")[0])
                print("size is " + str(leng))
                if vid not in urls and leng<20:
                    name = str(count) + ".mp4"
                    r  = requests.get(vid)
                    with open("media/temporary/web/" + name, 'wb') as f:
                        f.write(r.content)       
                urls.append(vid)
            except:
                print("error")
            time.sleep(5)   

            count+=1
            
            
class duck_duck:
    def youtube(url,folder):
        path = "media/temporary/" + folder + "/"
        exist = os.listdir(path)
        driver = webdriver.Chrome('/home/kir/Загрузки/chromedriver_linux64\chromedriver')
        URL = url
        driver.get(URL)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.find_all("div",{"class":"tile"})
        driver.close()
        blocks = [[i.find("img").get("alt"),i.get("data-link")] for i in blocks if i.get("data-link") and "youtube" in i.get("data-link")]
        path = "media/temporary/" + folder + "/"
        for j in blocks:
            name = j[0].replace(","," ") + ".mp4"
            if name not in exist:
                ydl_opts = {'outtmpl': path+name,"format":"18"}
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([j[1]])
                except:
                    pass  

        for i in os.listdir(path):
            if i.endswith(".mp4")==False:
                try:
                    os.remove(path+i)
                except:
                    shutil.rmtree(path+i, ignore_errors=True)
        
        

#delete_files("media/temporary/Политика")
#delete_files("media/temporary/Спорт")
#delete_files("media/temporary/Туризм")
#delete_files("media/temporary/Экономика")
#delete_files("media/temporary/Интернет")


#full_delete_files("media/temporary/Спорт")
#youtube_links.links("https://www.youtube.com/c/NBA/videos",'temporary',"Спорт",6)
#sport = ["https://www.youtube.com/results?search_query=sportsnet+nhl","https://www.youtube.com/results?search_query=SportsTalkLine+nba+games&sp=EgIIAg%253D%253D"]
#youtube.loads(sport,"Спорт")
#check_video_folder("media/temporary/Спорт")


#full_delete_files("media/temporary/Армия")
#on Sundays
#army = ["https://www.youtube.com/results?search_query=%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8+%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5+&sp=CAISBggCEAEYAQ%253D%253D","https://www.youtube.com/results?search_query=%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5+%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8&sp=CAASBggCEAEYAQ%253D%253D"]
#youtube.loads(army,"Армия")
#time loads 10.00 and 18.00
#time.sleep(10)
#youtube.archive("https://www.youtube.com/c/24NEWSplus/videos","weapon")


#full_delete_files("media/temporary/Происшествия")
#on Sundays
#cnage parser: "https://www.youtube.com/results?search_query=%D0%BF%D1%80%D0%B8%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F+%D1%80%D0%BE%D1%81%D1%81%D0%B8%D1%8F+24&sp=EgYIAhABGAE%253D"
#accidents = ["https://www.youtube.com/results?search_query=%D0%BF%D1%80%D0%BE%D0%B8%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F+%D1%87%D0%BF&sp=EgYIAhABGAE%253D","https://www.youtube.com/results?search_query=%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8+%D1%88%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D1%82%D0%B0+%D0%B4%D0%B5%D0%B2%D1%8F%D1%82%D1%8C+%D1%81+%D0%BF%D0%BE%D0%BB%D0%BE%D0%B2%D0%B8%D0%BD%D0%BE%D0%B9&sp=EgYIAhABGAE%253D","https://www.youtube.com/results?search_query=%D0%AD%D0%BA%D1%81%D1%82%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B2%D1%8B%D0%B7%D0%BE%D0%B2+112&sp=CAASBggCEAEYAQ%253D%253D","https://www.youtube.com/results?search_query=%D0%94%D0%BD%D0%B5%D0%BF%D1%80+%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9+LIVE&sp=EgQIAhgB",]
#youtube.loads(accidents,"Происшествия")
#time loads 10.00 and 18.00
#time.sleep(10)

#full_delete_files("media/temporary/Наука")
#science = ["https://www.youtube.com/results?search_query=+%D0%9D%D0%9E%D0%92%D0%9E%D0%A1%D0%A2%D0%98+%D0%9D%D0%90%D0%A3%D0%9A%D0%98+SCIENCE+NEWS+SCDAILY&sp=EgYIBBABGAE%253D"]
#youtube.loads(science,"Наука")
#time.sleep(10)

#full_delete_files("media/temporary/Авто")
#on Sundays
#auto = ["https://www.youtube.com/results?search_query=%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D1%80%D0%B5%D0%BD%D0%B4%D1%8B&sp=EgQIAhgB","https://www.youtube.com/results?search_query=%D0%B0%D0%B2%D1%82%D0%BE+%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8&sp=CAASBggDEAEYAQ%253D%253D","https://www.youtube.com/results?search_query=%D1%82%D0%B5%D1%81%D1%82+%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D1%8B+%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9&sp=EgQIBBgB"]
#youtube.loads(auto,"Авто")
#time.sleep(10)

#full_delete_files("media/temporary/Общество")
#full_delete_files("media/temporary/Мир")
#on Sundays
#delete_files("media/temporary/Общество")
#delete_files("media/temporary/Мир")
#video.izvestia()
#check_video_folder("media/temporary/Общество")
#check_video_folder("media/temporary/Мир")
#reload every 2 hours

##fun 10.00 and 18.00
full_delete_files("media/temporary/Развлечения")
video.y_pl()
video.press_fun()
check_video_folder("media/temporary/Развлечения")

#science links upload every day at 6.00 am
#full_delete_files("media/links/science")        
#youtube_links.links("https://www.youtube.com/c/QWRTru/videos",'qwerty',"science",4)
#youtube_links.links("https://www.youtube.com/c/prorobotov/videos",'pro_robots',"science",6)
#youtube_links.links("https://www.youtube.com/c/%D0%92%D0%A1%D0%95%D0%A1%D0%90%D0%9C%D0%9E%D0%95%D0%A1%D0%90%D0%9C%D0%9E%D0%95%D0%9D%D0%90%D0%9F%D0%9B%D0%90%D0%9D%D0%95%D0%A2%D0%95/videos",'techno',"science",1)
#youtube_links.links("https://www.youtube.com/c/KOSMOONE/videos",'kosmo',"science",2)
#youtube_links.links("https://www.youtube.com/user/MegaPeaceDuke/videos",'mad_science',"science",3)
#youtube_links.links("https://www.youtube.com/channel/UCcpNd-KO0b57e3sSr0ID0KQ/videos",'lovi_moment',"science",3)
#youtube_links.links("https://www.youtube.com/user/MasterskayaNastroeny/videos",'mn',"science",6)


##Movie reccomendation trailers
#full_delete_files("media/temporary/movies")
#youtube_links.movie_thrailers("https://www.youtube.com/c/iVideos/videos")


##webcam
#full_delete_files("media/temporary/web")
#web_cam.light()
#web_cam.medium("https://www.google.com/search?q=live+jasmin+video&tbs=qdr:d,srcf:H4sIAAAAAAAAAKvMLy0pTUrVS87PVdMuLkjMy05KzEsHc7Myq6ry85ITc8G8iozE3OKS1CIwpyC_1KM_1AQC-_1KB3MzChNAgsDAMTbga5NAAAA,dur:s&tbm=vid&sxsrf=ALeKk02yEFaLqXRPF7eIuO2mR_TTX2IvsQ:1609531808393&source=lnt&sa=X&ved=0ahUKEwiaksadxfvtAhUSmIsKHVwlBcQ4ChCnBQgm&biw=1600&bih=789&dpr=1")
#check_video_folder("media/temporary/web")

# django_remove()
# django_import()
