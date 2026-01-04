import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import os

# ==========================================
# 0. 日付決定ロジック (指定があればそれ、なければ明日)
# ==========================================
def get_target_date():
    # GitHub Actionsから渡された日付文字を取得
    input_date = os.environ.get('TARGET_DATE_INPUT', '').strip()
    
    if input_date:
        try:
            # 入力された日付 (YYYY-MM-DD) を解析
            return datetime.datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            print("日付形式エラー。明日に設定します。")
    
    # デフォルト: 明日
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=1)

# ==========================================
# 1. サイト別・特殊攻略部隊 (自動抽出)
# ==========================================

def scrape_tokyo_dome(target_date):
    """東京ドーム: 日付判定してイベント有無を返す"""
    url = "https://www.tokyo-dome.co.jp/dome/event/schedule.html"
    try:
        r = requests.get(url, timeout=10)
        r.encoding = r.apparent_encoding
        # 簡易チェック: 「1月5日」のような文字がページにあるか
        target_str = f"{target_date.month}月{target_date.day}日"
        if target_str in r.text:
             return f"18:00? 東京ドーム({target_str} イベント有 ❗️)"
        return ""
    except: return ""

def scrape_big_sight(target_date):
    """ビッグサイト"""
    url = "https://www.bigsight.jp/visitor/event/"
    try:
        r = requests.get(url, timeout=10)
        target_str = f"{target_date.month}/{target_date.day}" # ビッグサイトの表記に合わせる
        if target_str in r.text:
             return f"??:?? ビッグサイト({target_str} イベント有)"
        return ""
    except: return ""

def scrape_budokan(target_date):
    """武道館 (公式)"""
    url = "https://www.nipponbudokan.or.jp/schedule/"
    try:
        r = requests.get(url, timeout=10)
        # 武道館は画像が多いが、alt属性などに日付が入る可能性あり
        # 現状は簡易的に存在確認のみ
        return "" 
    except: return ""

# ==========================================
# 2. ターゲットリスト (全50サイト)
# ==========================================
# ここに自動抽出ロジック(func)を紐付けていきます
TARGET_SITES = [
    # --- あ行 ---
    {"name": "IMMシアター", "url": "https://imm.theater/schedule"},
    {"name": "青山学院記念館", "url": "https://spocale.com/places/77"},
    {"name": "有明アリーナ", "url": "https://ariake-arena.tokyo/event/"},
    {"name": "有明四季劇場", "url": "https://www.shiki.jp/sp_stage_schedule/?aj=0&rid=0057&ggc=4026#202512"},
    {"name": "EXシアター六本木", "url": "https://www.ex-theater.com/schedule/"},
    {"name": "NHKホール", "url": "https://www.nhk-fdn.or.jp/nhk_hall/event.html"},
    {"name": "大井競馬場", "url": "https://www.tokyocitykeiba.com/race/schedule/"},
    {"name": "オーチャードホール", "url": "https://www.bunkamura.co.jp/pickup/performance.html"},
    {"name": "オペラシティ", "url": "https://www.operacity.jp/concert/calendar/"},
    
    # --- か行 ---
    {"name": "ガーデンシアター", "url": "https://www.shopping-sumitomo-rd.com/tokyo_garden_theater/schedule/"},
    {"name": "勝島シアターH", "url": "https://theater-h.jp"},
    {"name": "歌舞伎座", "url": "https://www.kabuki-bito.jp/theaters/kabukiza/"},
    {"name": "芸術劇場", "url": "https://www.geigeki.jp/calendar/"},
    {"name": "JRA競馬", "url": "https://www.jra.go.jp/keiba/calendar/"},
    {"name": "国際フォーラム", "url": "https://www.t-i-forum.co.jp/visitors/event/"},
    {"name": "国立競技場", "url": "https://jns-e.com/event/"},
    
    # --- さ行 ---
    {"name": "サントリーホール", "url": "https://www.suntory.co.jp/suntoryhall/schedule/"},
    {"name": "四季劇場[海]", "url": "https://www.shiki.jp/stage_schedule/?aj=0&rid=0077&ggc=0905"},
    {"name": "品川プリンス クラブeX", "url": "https://www.princehotels.co.jp/shinagawa/clubex/"},
    {"name": "品川プリンス ステラボール", "url": "https://www.princehotels.co.jp/shinagawa/stellarball/"},
    {"name": "神宮球場", "url": "http://www.jingu-stadium.com/event/"},
    {"name": "新国立劇場", "url": "https://www.nntt.jac.go.jp/performance/calendar.html"},
    {"name": "新橋演舞場", "url": "https://www.shochiku.co.jp/play/theater/enbujyo/"},
    {"name": "すみだトリフォニー", "url": "https://www.triphony.com/concert/202512list.html"},
    {"name": "Zepp羽田", "url": "https://www.zepp.co.jp/hall/haneda/schedule/"},
    {"name": "セルリアン能楽堂", "url": "https://www.ceruleantower-noh.com/lineup/"},

    # --- た行 ---
    {"name": "第一ホテル東京", "url": "https://www.hankyu-hotel.com/hotel/dh/dhtokyo/events"},
    {"name": "宝塚劇場", "url": "https://kageki.hankyu.co.jp/sp/schedule/index.html"},
    {"name": "竹芝[東海汽船]", "url": "https://www.tokaikisen.co.jp/boarding/timetable/"},
    {"name": "竹芝四季劇場[春]", "url": "https://www.shiki.jp/stage_schedule/?aj=0&rid=0084"},
    {"name": "竹芝四季劇場[秋]", "url": "https://www.shiki.jp/stage_schedule/?aj=0&rid=0092"},
    {"name": "竹芝自由劇場", "url": "https://www.shiki.jp/stage_schedule/?aj=0&rid=0083"},
    {"name": "秩父宮ラグビー", "url": "https://www.jpnsport.go.jp/chichibunomiya/event/tabid/59/Default.aspx"},
    {"name": "椿山荘", "url": "https://hotel-chinzanso-tokyo.jp/event/"},
    {"name": "帝国ホテル", "url": "https://www.imperialhotel.co.jp/tokyo/event"},
    {"name": "東京會舘", "url": "https://www.kaikan.co.jp/news/event/index.html"},
    {"name": "東京ドーム", "url": "https://www.tokyo-dome.co.jp/dome/event/schedule.html", "func": scrape_tokyo_dome},
    {"name": "東京文化会館", "url": "https://www.t-bunka.jp/stage/"},
    {"name": "豊洲PIT", "url": "https://toyosu.pia-pit.jp"},
    {"name": "トヨタアリーナ", "url": "https://www.toyota-arena-tokyo.jp/events/"},

    # --- な行 ---
    {"name": "日生劇場", "url": "https://www.nissaytheatre.or.jp/schedule/"},
    {"name": "日本青年館", "url": "https://seinenkan-hall.com/category/performance"},
    {"name": "ニューオータニ", "url": "https://www.newotani.co.jp/tokyo/event/"},

    # --- は行 ---
    {"name": "ビッグサイト", "url": "https://www.bigsight.jp/visitor/event/", "func": scrape_big_sight},
    {"name": "武道館", "url": "https://www.nipponbudokan.or.jp/schedule/", "func": scrape_budokan},
    {"name": "ブルーノート", "url": "https://reserve.bluenote.co.jp/reserve/mb_schedule/"},
    {"name": "文京シビック", "url": "https://www.b-academy.jp/hall/calendar.html"},
    {"name": "ベイコート倶楽部", "url": "https://www.rtg.jp/hotels/bcc/tokyo/event/"},
    {"name": "平和島競艇", "url": "https://www.heiwajima.gr.jp/sp/01cal/01cal.htm"},

    # --- ま・や・ら行 ---
    {"name": "明治座", "url": "https://www.meijiza.co.jp/info/"},
    {"name": "代々木第一", "url": "https://www.jpnsport.go.jp/yoyogi/event/tabid/59/Default.aspx"},
    {"name": "代々木第二", "url": "https://www.jpnsport.go.jp/yoyogi/event/tabid/60/Default.aspx"},
    {"name": "両国国技館", "url": "https://kokugikan.sumo.or.jp/Schedule/show"}
]

def run_crawler():
    results = []
    target_date = get_target_date()
    date_str = f"{target_date.month}月{target_date.day}日"
    weekday = ["月","火","水","木","金","土","日"][target_date.weekday()]
    
    print(f"Target Date: {date_str} ({weekday})")

    # メタデータ（日付情報）
    results.append({
        "type": "meta",
        "date_str": f"{date_str} ({weekday})"
    })

    # サイト巡回
    for site in TARGET_SITES:
        info_text = ""
        
        # 専用の抽出ロジックがある場合
        if "func" in site and site["func"] is not None:
            extracted = site["func"](target_date)
            if extracted:
                info_text = extracted
            else:
                info_text = f"??:??  {site['name']}(イベントなし?)"
        else:
            # 汎用
            info_text = f"??:??  {site['name']}(??:??-  )"

        # 結果追加
        results.append({
            "type": "data",
            "venue": site['name'],
            "info": info_text,
            "url": site['url']
        })
        time.sleep(0.5)

    with open('event_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_crawler()
