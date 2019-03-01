#namuWiki_TomHardy_scraper.py
#나무위키에서 톰하디 페이지 중 본문에 해당하는 내용 중, 하이퍼링크의 제목과 url을 가져와서 csv파일로 저장하기
#구체적으로 selenium으로 https://namu.wiki를 접속한 후 검색창에 톰하디를 치고 검색까지 누른다
#requests 모듈로 해당 url을 res라는 변수에 저장한다
#BeautifulSoup으로 html을 parsing해서 그 중 태그가 <a href=인 것을 가져오는데, 텍스트만 가져오고 주소 앞에 http://namu.wiki를 붙인다
#모든 링크를 리스트 형태로 가져와서
#pandas로 csv 파일을 저장한다.
#단 폴더는 현재 폴더를 부른 후 그 상위 폴더에 폴더를 새로 만들고(namuWiki_TomHardy_scraper) 저장한다
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


browser = webdriver.Chrome('C:\\Users\\Multimilinaire\\Downloads\\chromedriver.exe')
#chrome이라고 쓰면 안되고 대문자로 써야됨

keyWord = '사쿠라지마 마이'
url = 'https://namu.wiki/w/' + keyWord
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')


#########select 써서 하는거 포기했다가 다시 도전함. select와 find를 같이 써보려니까 망한거임. 단계를 나누면됨

#존나 어려워서 포기하고 find_all로 도전해본 흔적
#for link in soup.find_all('a'):
#    namuTitle = link.get('title'))
#타이틀명을 뽑아오기
#for link in soup.find_all('a'):
#    print(link.get('href'))
#링크를 뽑아오기
#본문의 a태그 중에서 title요소의 값을 namuTitle변수에 리.스.트로 저장
#따라서 for뤂으로 하나씩 꺼내야

wikiLinkInt = soup.select('.wiki-link-internal')
myNamuLink = []
for link in wikiLinkInt:
        thTitle = link.get('title')
        thRef_ko = 'http://namu.wiki/w/' + thTitle
        #thRef = 'http://namu.wiki' + link.get('href') 이렇게 하면 주소가 특수문자로 나오는데 위와 같이 하면 한글로 표기됨
        myNamuLink.append((thTitle,thRef_ko))

#판다스에서 저장!!
df = pd.DataFrame(myNamuLink,columns=['title','링크'])
#df.to_csv('C:\\Users\\Multimilinaire\\Desktop\\boring webscraper\\namuwikiscraper\\'+ keyWord + '.csv')
df.to_excel('C:\\Users\\Multimilinaire\\Desktop\\boring webscraper\\namuwikiscraper\\'+ keyWord + '.xlsx',index=False)
#df.to_json('C:\\Users\\Multimilinaire\\Desktop\\boring webscraper\\namuwikiscraper\\'+ keyWord + '.json')
dfString = df.applymap(str)

#개쩐다...존나 신기하다

#나의 Pyson블로그에 자동으로 글을 올리는걸 해보자

browser = webdriver.Chrome('C:\\Users\\Multimilinaire\\Downloads\\chromedriver.exe')
browser.get('http://pyson.pythonanywhere.com/admin')
idElem = browser.find_element_by_id('id_username')
idElem.send_keys('Pyson')
pwElem = browser.find_element_by_id('id_password')
pwElem.send_keys('game11..')
pwElem.submit()

browser.get('http://pyson.pythonanywhere.com/')

browser.find_element_by_css_selector('body > div.page-header > a > span').click()

ttlElem = browser.find_element_by_id('id_title')
ttlElem.send_keys(keyWord)
txtElem = browser.find_element_by_id('id_text')
txtElem.send_keys(str(myNamuLink))
#txtElem.send_keys(keyWord + ' 나무위키 scraping 성공')
browser.find_element_by_css_selector('body > div.content.container > div > div > form > button').click()
browser.quit()