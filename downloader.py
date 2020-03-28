import os
import time
import pytube

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# youtube credentials and the music folder
username =
password =
folder =
try:
    os.mkdir(folder+'/songs')
except FileExistsError:
    print("Directory ", folder, " already exists")

browser = webdriver.Chrome('C:/Users/rosen/Downloads/chromedriver_win32/chromedriver.exe')
browser.get('https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Diw%26next%3D%252Ffeed%252Fhistory&hl=he')
browser.find_element_by_id("identifierId").send_keys(username)
browser.find_element_by_id("identifierNext").click()
time.sleep(1)
browser.find_element_by_css_selector("input[type='password']").send_keys(password)
browser.find_element_by_id("passwordNext").click()
element_present = EC.presence_of_element_located((By.ID, 'contents'))
WebDriverWait(browser, 100).until(element_present)
time.sleep(5)
for i in range(10):
    browser.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(1)
page = browser.page_source
browser.close()
videos = page.split("<ytd-video-renderer")
links = []
videos.pop(0)
if os.path.isfile(folder + "/downloaded videos.txt"):
    file = open(folder + "/downloaded videos.txt", "r")
    downloadedVideos = file.read().split('\n')
    file.close()
else:
    downloadedVideos = []
for video in videos:
    link = video.split('href="')[1]
    link = link.split('"')[0].split("&")[0]
    if 'https://youtube.com' + link not in downloadedVideos:
        links.append(link)
links = list(dict.fromkeys(links))
songs = []
lastprogress=-1
browser = webdriver.Chrome('C:/Users/rosen/Downloads/chromedriver_win32/chromedriver.exe')
for link in links:
    progres=(links.index(link)/len(links))*100
    if progres - lastprogress>1:
        print(str(progres)+"%     "+ str(len(links)) + " total" )
        lastprogress = progres
    browser.get('https://youtube.com' + link)
    element_present = EC.presence_of_element_located((By.ID, 'more'))
    WebDriverWait(browser, 100).until(element_present)
    more = browser.find_element_by_id('more')
    try:
        more.click()
    except:
        print("no more")
    div = browser.find_element_by_id('meta')
    if 'href="/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ"' in div.get_attribute('innerHTML'):
        songs.append('https://youtube.com' + link)
browser.close()
f=open(folder + "/downloaded videos.txt", 'a+')
failedsongs=[]
for song in songs:
    try:
        youtube = pytube.YouTube(song)
        print("downloading "+youtube.title)
        video = youtube.streams.first()
        video.download(folder+'/songs')
        f.write("%s\n" % song)
        time.sleep(1)
    except:
        failedsongs.append(song)
f.close()
with open(folder + "/failed videos.txt","w+") as f:
    for failed in failedsongs:
        f.write("%s\n" % failed)
