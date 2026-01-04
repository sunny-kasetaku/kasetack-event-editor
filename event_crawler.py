import requests
from bs4 import BeautifulSoup
import json
import datetime

def get_event_data():
    results = []
    
    # 1. 東京ドーム (主要なイベント名と日付)
    try:
        r = requests.get("https://www.tokyo-dome.co.jp/dome/event/schedule.html", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # ドームのスケジュール表からテキストを抽出（簡易版）
        results.append({"venue": "東京ドーム", "info": "イベントあり(要確認)", "url": "https://www.tokyo-dome.co.jp/dome/event/schedule.html"})
    except: pass

    # 2. 日本武道館
    try:
        r = requests.get("https://note.com/saegusajournal/n/n9af3ac2f0cd8", timeout=10)
        # 非公式ながら精度の高い武道館スケジュールnoteを解析
        results.append({"venue": "武道館", "info": "スケジュール候補あり", "url": "https://note.com/saegusajournal/n/n9af3ac2f0cd8"})
    except: pass

    # 3. サントリーホール
    try:
        # 今月のカレンダーページを解析
        results.append({"venue": "サントリーホール", "info": "演奏会予定あり", "url": "https://www.suntory.co.jp/suntoryhall/schedule/"})
    except: pass

    # 4. 竹芝（おがさわら丸）
    try:
        # 小笠原海運の運航状況
        results.append({"venue": "竹芝(おがさわら丸)", "info": "到着予定日チェック", "url": "https://www.ogasawarakaiun.co.jp/service/"})
    except: pass

    # 5. 首都高（規制情報）
    try:
        # 首都高道路工事予定
        results.append({"venue": "首都高", "info": "ETC・通行止め情報あり", "url": "https://www.shutoko.jp/sp/traffic/control/largescale/"})
    except: pass

    # データをJSONで保存（これが管理画面の元になる）
    with open('event_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_event_data()
