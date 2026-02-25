import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def get_urls(header):
    melon_url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100"
    root_url = "https://www.melon.com"
    gen_dic = {}
    melon_raw = requests.get(melon_url, headers=header)
    melon_bs = BeautifulSoup(melon_raw.text, "html.parser")
    tab_names = melon_bs.find("div", {"class" : "wrap_tabmenu01 type08"}).find_all("li") # 탭 영역 전체 
    for tab_name in tab_names:
        gen_dic[tab_name.text] = root_url+tab_name.find("a").attrs['href'] # a 태그 안에 있는 href 요소를 갖고 온다. 
    return gen_dic

def get_song_info(gen_url, header):
    gen_raw = requests.get(gen_url, headers=header)
    gen_bs = BeautifulSoup(gen_raw.text, "html.parser")
    daily_gen_top_50 = gen_bs.find("div", id="songList").find("tbody").find_all("tr")
    songs = [] # 노래와 가수를 담을 빈 리스트
    singers = []
    for daily_gen_top in daily_gen_top_50:
        song = daily_gen_top.find("div", class_ = "wrap_song_info").find_all("a")[0].text
        singer = daily_gen_top.find("div", class_ = "wrap_song_info").find_all("a")[1].text
        songs.append(song)
        singers.append(singer)
    return songs, singers

def print_rank(songs: list, singers: list, text_widget):
    text_widget.delete(1.0, tk.END)  # Clear previous content
    for rank, song_info in enumerate(zip(songs, singers)):
        singer, song = song_info
        text_widget.insert(tk.END, f"{rank+1} : {singer} : {song}\n")

# 실제 동작 나열 
def main():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    urls = get_urls(header)
    
    root = tk.Tk()
    root.title("Melon Genre Song Rankings")
    root.resizable(True, True)  # Allow window resizing
    
    tk.Label(root, text="장르를 선택하세요:").pack(pady=10)
    genre_var = tk.StringVar()
    genre_combo = ttk.Combobox(root, textvariable=genre_var, values=list(urls.keys()), state="readonly")
    genre_combo.pack(pady=5)
    
    text_area = tk.Text(root, height=20, width=50)
    text_area.pack(pady=10, fill=tk.BOTH, expand=True)
    
    def fetch_rankings():
        selected_genre = genre_var.get()
        if selected_genre in urls:
            gen_url = urls[selected_genre]
            songs, singers = get_song_info(gen_url, header)
            print_rank(songs, singers, text_area)
    
    tk.Button(root, text="순위 가져오기", command=fetch_rankings).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
