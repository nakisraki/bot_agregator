from  yahoo_fin import stock_info as si
#from yahoofinancials import YahooFinancials
from datetime import datetime
from lxml import html
import re
from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import cryptocompare
day_of_week = datetime.today().strftime('%A')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


class Finance:
    def base_price():
        text = ''
        ##Crypto
        values = si.get_top_crypto()
        btc = values.iloc[0]
        price = btc["Price (Intraday)"]
        percent = btc["% Change"]
        arrow = ""
        if float(percent)>0:
            arrow = "↑"
        else:
            arrow = "↓"
        text = text + "\U0001F171 Биткоин (BTC)  " + str(price) + " " + arrow + str(percent) + "%" + "\n"
        ##Gold and Oil
        html = "https://oilprice.com/oil-price-charts/46"
        full_page = requests.get(html,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        blocks = soup.find("tr",{"data-spreadsheet":"Crude Oil Brent"})
        price = blocks.find("td",{"class":"last_price"}).get("data-price")
        try:
            change = blocks.find("td",{"class":"change_up_percent percent_change_cell"}).text.replace("+","↑").replace("-","↓").replace("%","%  ")
        except:
            change = blocks.find("td",{"class":"change_down_percent percent_change_cell"}).text.replace("+","↑").replace("-","↓").replace("%","%  ")
        oil = "\U0001F6E2 Нефть(Brent)  "  + str(price) + "  " + change.split("(")[0] + "\n"
        text = text + oil
        html = "https://www.kitco.com/charts/livegold.html"
        full_page = requests.get(html,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        price = soup.find("div",{"class":"data-blk ask"}).text.replace("Ask","/Oz")
        change = soup.find("span",{"id":"sp-chg-percent"}).text.replace("+","↑").replace("-","↓")
        gold = "\U0001F3C5 Золото " + price + " " + change + "\n"
        text = text + gold
        return text

    def upcoming_ipo():
        url = "https://www.iposcoop.com/ipo-calendar/"
        full_page = requests.get(url,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        ipos = soup.find_all("tr")[1:]
        if len(ipos)==1:
            return []
        data = {}
        for i in ipos:
            content = i.find_all("td")
            if int(content[6].text.split(" ")[1].split(".")[0])>=500:
                data[content[0].text] = {"Symbol":content[1].text,"Capitalization":content[6].text.split(" ")[1],"Date":content[7].text.split(" ")[0]}
                html = content[0].find("a").get("href")
                full_page = requests.get(html,headers=headers)
                soup = BeautifulSoup(full_page.content, 'html.parser')
                row = soup.find_all("tr")
                data[content[0].text]["Revenue"] = row[12].text.replace("\n","").split("$")[1]
                data[content[0].text]["Net-Income"] = row[13].text.replace("\n","").split("$")[1]
                data[content[0].text]["Web-Site"] = row[8].find("a").get("href")
        ipos = []
        for i in data:
            text = data[i]["Date"] + "\n" + i + "\n" + "Оценка : " + data[i]["Capitalization"] + " милл. " + "\n" + "Общий доход : " + data[i]["Revenue"].replace("mil (last 12 months)","милл. (12 месяцев)") + "\n" + "Чистая прибыль : " + data[i]["Net-Income"].replace("mil (last 12 months)","милл. (12 месяцев)")
            next_month_graph = "-"
            ipos.append([text,data[i]["Web-Site"],next_month_graph])
        return ipos

    def crypto():
        btc = cryptocompare.get_price('BTC',curr='USD')['BTC']['USD']
        btc_day_ago = cryptocompare.get_historical_price_day('BTC', curr='USD', limit=1)[0]['open']
        btc_percent = round(100 * (btc-btc_day_ago) / btc_day_ago , 2)
        eth = cryptocompare.get_price('ETH',curr='USD')['ETH']['USD']
        eth_day_ago = cryptocompare.get_historical_price_day('ETH', curr='USD', limit=1)[0]['open']
        eth_percent = round(100 * (eth-eth_day_ago) / eth_day_ago, 2)
        btc_text , eth_text = '',''
        if btc_percent>0:
            btc_text = str(btc) + " ↑  +" + str(btc_percent) + "%"
        else:
            btc_text = str(btc) + " ↓  " + str(btc_percent) + "%"
        if eth_percent>0:
            eth_text = str(eth) + " ↑  +" + str(eth_percent) + "%"
        else:
            eth_text = str(eth) + " ↓  " + str(eth_percent) + "%"
        data = [btc_text + " (24 часа)",eth_text+ " (24 часа)"]
        return data

        
class Sport:
    def sport_line_change():
        url = "https://betzona.ru/dropping-odds"
        full_page = requests.get(url,headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        games = soup.find_all("div",{"class":"match"})
        matches = []
        for i in games[:12]:
            data = {}
            game = i.find("div",{"class":"match_name"}).text
            league = i.find("div",{"class":"tournament_name"}).text
            result = i.find("div",{"class":"col-8 odd_type"}).text
            values = i.find("div",{"class":"ratios"}).text.split("\n")
            values = [float(i) for i in values if i!= '']
            start,now = values[0],values[1]
            change = str(int((start-1.0)/(now-1.0)*100/2)) + " %"
            data['game'],data['league'],data['result'] = game,league,result
            data['start'],data['now'],data['change'] = start,now,change
            pref = ""
            if "Баскетбол" in league:
                pref = "\U0001F3C0"
            elif "Футбол" in league:
                pref = "\U0001F3D0"
            elif "Хоккей" in league:
                pref =  "\U0001F3D2"
            elif "Теннис" in league:
                pref =  "\U0001F3BE"
            elif "Воллейбол" in league:
                pref =  "\U0001F3D0"
            else:
                pref = "\U0001F94F"
            text = pref + " " + data["league"] + "\n" + data['game'] + "  " + data['result'] + "  старт:" + str(values[0]) + "  cейчас:" + str(values[1]) + "\n" + "Изменение:" + change
            if now<=2.0:
                matches.append(text)
        return matches
        
       
