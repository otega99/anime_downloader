import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

def get_webpage(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(url)
    html=driver.page_source
    page_soup=soup(html,"html.parser")
    driver.quit()
    return page_soup

def get_all_videos(question):
    answer=input(question)
    if answer=='y':
        return True
    elif answer=='n':
        return False
    else:
        return download_all("Please enter y or n: ")
        
def check_number(question,episodes_dict):
    number=input(question)
    if number in episodes_dict:
        return number
    else:
        return check_number("This does not exist, please enter another number: ",episodes_dict)
       
def download_episode(anime_name,selected_episode,episodes_dict):
    selected_episode_webpage=get_webpage(episodes_dict[selected_episode]["link"])
    downloads_link=selected_episode_webpage.findAll("li",{"class":"dowloads"})[0].a["href"]
    downloads_webpage=get_webpage(downloads_link)
    video_link=downloads_webpage.findAll("div",{"class":"mirror_link"})[0].findAll("div",{"class":"dowload"})[0].a["href"]
    path="/home/tega/Videos/Anime/"+anime_name
    if os.path.exists(path)==False:
        os.mkdir(path)
    file_name=video_link.split('/')[-1]
    print("Downloading file {}".format(file_name))
    episode_path=path+"/"+file_name
    r=requests.get(video_link,stream=True)    
    with open(episode_path,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    print("Downloaded {} !".format(file_name))
    
    
        
        
