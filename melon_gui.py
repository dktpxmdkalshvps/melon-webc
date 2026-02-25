import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_melon_chart():
    input_genre = genre_combo.get()
    
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

    if input_genre not in music_genres:
        messagebox.showwarning("알림", "장르를 선택해주세요.")
        return

    try:
        # 데이터 크롤링 시작
        melon_url = f"https://www.melon.com/genre/song_list.htm?gnrCode={music_genres[input_genre]}"
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        melon_raw = requests.get(melon_url, headers=header)
        
        # pandas의 read_html을 사용하여 테이블 추출
        # 멜론 웹페이지 구조에 맞춰 첫 번째 테이블 사용
        df_list = pd.read_html(melon_raw.text)
        melon_top50_df = df_list[0]
        
        # 기존 표 내용 삭제
        for i in tree.get_children():
            tree.delete(i)

        # 데이터 프레임의 '곡정보' 컬럼 데이터를 표에 삽입
        # 멜론 테이블 구조상 50위까지 추출
        for idx, row in melon_top50_df[:50].iterrows():
            # '곡정보' 텍스트 정리 (불필요한 공백 및 '곡정보' 단어 제거 등)
            song_info = str(row['곡정보']).replace('곡정보', '').strip()
            tree.insert('', 'end', values=(idx + 1, song_info))

    except Exception as e:
        messagebox.showerror("오류", f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

# --- GUI 설정 ---
root = tk.Tk()
root.title("Melon 장르별 Top 50 조회기")
root.geometry("500x600")

# 상단 레이블 및 선택창 영역
frame_top = tk.Frame(root, pady=10)
frame_top.pack()

tk.Label(frame_top, text="장르 선택: ").grid(row=0, column=0, padx=5)

genre_list = ["발라드", "댄스", "랩/힙합", "R&B/Soul", "인디음악", "록/메탈", "트로트", "포크/블루스"]
genre_combo = ttk.Combobox(frame_top, values=genre_list, state="readonly")
genre_combo.current(0)
genre_combo.grid(row=0, column=1, padx=5)

btn_search = tk.Button(frame_top, text="조회하기", command=get_melon_chart, bg="#00cd3c", fg="white", font=('NanumGothic', 9, 'bold'))
btn_search.grid(row=0, column=2, padx=5)

# 하단 결과 표 영역
frame_bottom = tk.Frame(root)
frame_bottom.pack(fill="both", expand=True, padx=10, pady=10)

# 표(Treeview) 생성
columns = ("rank", "info")
tree = ttk.Treeview(frame_bottom, columns=columns, show='headings')
tree.heading("rank", text="순위")
tree.heading("info", text="곡 정보 (곡명 / 아티스트)")
tree.column("rank", width=50, anchor="center")
tree.column("info", width=400)

# 스크롤바 추가
scrollbar = ttk.Scrollbar(frame_bottom, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()