import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

input_genre = input("장르를 입력하세요 (발라드, 댄스, 랩/힙합, R&B/Soul, 인디음악, 록/메탈, 트로트, 포크/블루스): ")

music_genres = {
    "발라드": "GN0100",
    "댄스": "GN0200",
    "랩/힙합": "GN0300",
    "R&B/Soul": "GN0400",
    "인디음악": "GN0500",
    "록/메탈": "GN0600",
    "트로트": "GN0700",
    "포크/블루스": "GN0800"
}

melon_url = f"https://www.melon.com/genre/song_list.htm?gnrCode={music_genres[input_genre]}"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
melon_raw = requests.get(melon_url, headers=header)
melon_bs = bs(melon_raw.text, "html.parser")
melon_top50_df = pd.read_html(melon_raw.text)[0]
melon_top50_df[:50][['곡정보']]