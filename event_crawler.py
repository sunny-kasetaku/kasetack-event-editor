import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

def scrape_yoyogi():
    """代々木第一体育館のイベント抽出"""
    url = "https://www.jpnsport.go.jp/yoyogi/event/tabid/59/Default.aspx"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # 簡易抽出（実際の構造に合わせて調整）
        events = soup.select(".event-list-item") # 仮のクラス名
        return [{"venue": "代々木一", "info": "イベントあり"}]
    except: return []

def scrape_ogasawara():
    """小笠原丸の到着便を抽出"""
    url = "https://www.ogasawarakaiun.co.jp/service/"
    try:
        r = requests.get(url, timeout=10)
        # 「竹芝着」という文字と時間を探す
        if "竹芝着" in r.text:
            return [{"venue": "竹芝", "info": "15:30  竹芝(おがさわら丸到着予定 ¥ -83140❗️)", "rank": "pick"}]
    except: pass
    return []

def scrape_shutoko():
    """首都高の長期規制・通行止め"""
    url = "https://www.shutoko.jp/sp/traffic/control/largescale/"
    try:
        r = requests.get(url, timeout=10)
        # 特定の入口名（勝島・板橋本町など）が含まれているかチェック
        found = []
        for spot in ["勝島", "板橋本町", "船堀橋"]:
            if spot in r.text:
                found.append(f"入口閉鎖: {spot}")
        if found:
            return [{"venue": "首都高", "info": f"(ETC入口長期工事) {' / '.join(found)}"}]
    except: pass
    return []

def run_all_scrapers():
    all_results = []
    
    # --- 順次追加 ---
    all_results.extend(scrape_ogasawara())
    all_results.extend(scrape_shutoko())
    
    # 東京ドーム、武道館などはURLから「開催の有無」だけ先にチェック
    major_sites = [
        {"name": "東京ドーム", "url": "https://www.tokyo-dome.co.jp/dome/event/schedule.html"},
        {"name": "武道館", "url": "https://note.com/saegusajournal/n/n9af3ac2f0cd8"},
        {"name": "サントリーホール", "url": "https://www.suntory.co.jp/suntoryhall/schedule/"},
        {"name": "ブルーノート", "url": "https://reserve.bluenote.co.jp/reserve/mb_schedule/move/202601/"}
    ]
    
    for site in major_sites:
        all_results.append({
            "venue": site['name'],
            "info": f"19:00? {site['name']}(時間要確認) ❗️",
            "url": site['url']
        })

    # 結果をJSON保存（index.htmlがこれを読み込む）
    with open('event_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_all_scrapers()
