import requests
from bs4 import BeautifulSoup
import json
import datetime
import re
import time

# ==========================================
# 1. ターゲットリスト (サニーPのリスト完全版)
# ==========================================
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
    {"name": "東京ドーム", "url": "https://www.tokyo-dome.co.jp/dome/event/schedule.html"},
    {"name": "東京文化会館", "url": "https://www.t-bunka.jp/stage/"},
    {"name": "豊洲PIT", "url": "https://toyosu.pia-pit.jp"},
    {"name": "トヨタアリーナ", "url": "https://www.toyota-arena-tokyo.jp/events/"},

    # --- な行 ---
    {"name": "日生劇場", "url": "https://www.nissaytheatre.or.jp/schedule/"},
    {"name": "日本青年館", "url": "https://seinenkan-hall.com/category/performance"},
    {"name": "ニューオータニ", "url": "https://www.newotani.co.jp/tokyo/event/"},

    # --- は行 ---
    {"name": "ビッグサイト", "url": "https://www.bigsight.jp/visitor/event/"},
    {"name": "武道館", "url": "https://www.nipponbudokan.or.jp/schedule/"}, # 公式に変更
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

# ==========================================
# 2. 特殊部隊 (特定のサイト専用ロジック)
# ==========================================
def check_ogasawara():
    """小笠原丸の竹芝到着を判定"""
    url = "https://www.ogasawarakaiun.co.jp/service/"
    try:
        r = requests.get(url, timeout=10)
        r.encoding = r.apparent_encoding
        # 今日の日付（例：1/5）を作成
        today = datetime.datetime.now()
        date_str = f"{today.month}/{today.day}"
        
        # 簡易判定：「竹芝着」と「今日の日付」が近くにあれば反応
        if "竹芝着" in r.text:
            # 本来は日付判定を厳密にするが、まずは存在確認
            return {
                "venue": "竹芝(おがさわら丸)",
                "info": "15:30  竹芝(おがさわら丸到着? 要確認 ¥-83140❗️)",
                "url": url,
                "is_special": True
            }
    except: pass
    return None

def check_shutoko():
    """首都高の長期工事・通行止め"""
    url = "https://www.shutoko.jp/sp/traffic/control/largescale/"
    try:
        r = requests.get(url, timeout=10)
        r.encoding = r.apparent_encoding
        found_spots = []
        # キーワードリスト
        targets = ["勝島", "板橋本町", "船堀橋", "大師", "平和島"]
        for t in targets:
            if t in r.text:
                found_spots.append(t)
        
        if found_spots:
            return {
                "venue": "首都高",
                "info": f"(ETC入口長期工事) {' / '.join(found_spots)}",
                "url": url,
                "is_special": True
            }
    except: pass
    return None

# ==========================================
# 3. 汎用部隊 (とりあえず全サイト回るくん)
# ==========================================
def run_crawler():
    results = []
    
    # 特殊部隊の実行
    oga = check_ogasawara()
    if oga: results.append(oga)
    
    shu = check_shutoko()
    if shu: results.append(shu)

    # 汎用部隊の実行
    # 今は「サイト名」と「空欄のひな形」を作る
    # (将来的にここに各サイトごとの解析ロジックを追加していく)
    
    # 今日の日付
    d = datetime.datetime.now()
    today_str = f"{d.month}/{d.day}"

    print(f"Crawling {len(TARGET_SITES)} sites...")
    
    for site in TARGET_SITES:
        # 特殊部隊ですでに取れている場合はスキップしない（重複チェックなし）
        
        # 基本フォーマットを作成
        # 例: 18:00? 東京ドーム(16:00- イベント名 ¥10000)
        # 初期値は空欄にして、スタッフが入力しやすくする
        info_text = f"??:??  {site['name']}(??:??-  )"
        
        results.append({
            "venue": site['name'],
            "info": info_text,
            "url": site['url'],
            "is_special": False
        })
        
        # サーバー負荷軽減のため0.5秒待つ
        time.sleep(0.5)

    # JSON保存
    with open('event_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Done!")

if __name__ == "__main__":
    run_crawler()
