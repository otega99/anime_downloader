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
    selection_prompt="\nPlease enter the number of episode you wish to download ,1-{}: ".format(len(episode_list))
    selected_episode=web.check_number(selection_prompt,episodes_dict)
    web.download_episode(selected_anime_name,selected_episode,episodes_dict)
else:
    for key, value in episodes_dict.items():
        web.download_episode(selected_anime_name,key,episodes_dict)
        