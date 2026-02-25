import requests
from bs4 import BeautifulSoup
def get_urls(header):
    melon_url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100"
    root_url = "https://www.melon.com"
    gen_dic = {}
    melon_raw = requests.get(melon_url, headers=header)
    melon_bs = BeautifulSoup(melon_raw.text, "html.parser")
    tab_names = melon_bs.find("div", {"class" : "wrap_tabmenu01 type08"}).find_all("li")
    for tab_name in tab_names:
        gen_dic[tab_name.text] = root_url+tab_name.find("a").attrs['href']
    return gen_dic


def get_song_info(gen_url, header):
    gen_raw = requests.get(gen_url, headers=header)
    gen_bs = BeautifulSoup(gen_raw.text, "html.parser")
    daily_gen_top_50 = gen_bs.find("div", id="songList").find("tbody").find_all("tr")
    songs = []
    singers = []
    for daily_gen_top in daily_gen_top_50:
        song = daily_gen_top.find("div", class_ = "wrap_song_info").find_all("a")[0].text
        singer = daily_gen_top.find("div", class_ = "wrap_song_info").find_all("a")[1].text
        songs.append(song)
        singers.append(singer)
    return songs, singers
def print_rank(songs, singers):
    for rank, song_info in enumerate(zip(songs, singers)):
        singer, song = song_info
        print(f"{rank+1} : {singer} : {song}")


def main():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    urls = get_urls(header)
    user_input = ""
    for i in urls.keys():
        print(f"{i}")
    while user_input not in urls.keys():
        user_input = input("장르를 입력 하세요 : ")
    gen_url = urls[user_input]
    songs, singers = get_song_info(gen_url, header)
    print_rank(songs, singers)
if __name__ == "__main__":
    main()