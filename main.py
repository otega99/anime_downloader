import web

main_url="https://www1.gogoanime.ai"
anime=input("Please enter the anime you want to download: ").replace(" ","%20")
search_url=main_url+"//search.html?keyword="+anime

results_webpage=web.get_webpage(search_url)
results_dict={}
results=results_webpage.findAll("p",{"class":"name"})
count=0

for result in results:
    results_dict[str(count)]={"name":result.text,"link":main_url+result.a["href"]}
    print("{}.{}".format(count,result.text))
    count+=1
    
try:
    selected_anime=input("\nPlease select the number of the anime you would like to watch: ")
except:
    selected_anime=input("\nPlease enter a valid number: ")

selected_anime_name=results_dict[selected_anime]["name"]
selected_anime_url=results_dict[str(selected_anime)]["link"]
selected_anime_webpage=web.get_webpage(selected_anime_url)



episodes_dict={}
episode_list=selected_anime_webpage.find(id="episode_related").findAll("li")
count=len(episode_list)
for episode in episode_list:
    episodes_dict[str(count)]={"name":"episode-"+str(count),"link":main_url+episode.a["href"].lstrip()}
    count-=1

count=0
question="\nDo you wish to download all episodes at once? (y/n) "

if web.get_all_videos(question)==False:
    selection=input("\nPlease enter the number of episode or episodes you wish to download from 1-{} (e.g 1, 3-10): ".format(len(episode_list)))
    selected_episodes=selection.split("-")
    if len(selected_episodes)==1:
        if selection in episodes_dict:
            web.download_episode(selected_anime_name,selection,episodes_dict)
        else:
            print("Episode not found")
    else:
        first_episode=int(selected_episodes[0])
        last_episode=int(selected_episodes[-1])+1
        for i in range(first_episode,last_episode):
            if str(i) in episodes_dict:
                web.download_episode(selected_anime_name,str(i),episodes_dict)      
            else:
                print("Episode not found")      
else:
    for key, value in episodes_dict.items():
        web.download_episode(selected_anime_name,key,episodes_dict)
        