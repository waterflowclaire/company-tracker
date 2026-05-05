import json
import os
import time
from datetime import datetime, timezone, timedelta
import requests

TW = timezone(timedelta(hours=8))
today = datetime.now(TW).strftime('%Y%m%d')
today_label = datetime.now(TW).strftime('%Y-%m-%d')

API_BASE = 'https://data.gcis.nat.gov.tw/od/data/api/236EE397-4D4A-4E7B-9A81-D27C0EB1CB1E'
DATA_DIR = 'data'
MAX_RECORDS = 1000
BATCH = 200

os.makedirs(DATA_DIR, exist_ok=True)

def fetch_all():
    results = []
    skip = 0
    while skip < MAX_RECORDS:
        params = {'$format': 'json', '$skip': skip, '$top': BATCH}
        try:
            resp = requests.get(API_BASE, params=params, timeout=30)
            resp.raise_for_status()
            batch = resp.json()
        except Exception as e:
            print(f'[錯誤] skip={skip}: {e}')
            break
        if not batch:
            break
        results.extend(batch)
        print(f'  已取得 {len(results)} 筆...')
        if len(batch) < BATCH:
            break
        skip += BATCH
        time.sleep(1)
    return results

def normalize(records, fetch_date):
    out = []
    for r in records:
        out.append({
            'biz_no': r.get('Business_Accounting_NO', '').strip(),
            'name': r.get('Company_Name', '').strip(),
            'date': r.get('Change_Of_Approval', '').strip(),
            'fetch_date': fetch_date,
        })
    return out

def main():
    print(f'[{today_label}] 開始抓取...')
    raw = fetch_all()
    print(f'共取得 {len(raw)} 筆原始資料')
    records = normalize(raw, today_label)

    daily_file = os.path.join(DATA_DIR, f'{today}.json')
    with open(daily_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'已儲存: {daily_file}')

    index_file = os.path.join(DATA_DIR, 'index.json')
    history = []
    if os.path.exists(index_file):
        with open(index_file, encoding='utf-8') as f:
            old = json.load(f)
            history = old.get('history', [])

    if today_label not in history:
        history.insert(0, today_label)
    history = history[:30]

    index = {
        'latest': today_label,
        'latest_count': len(records),
        'updated_at': datetime.now(TW).isoformat(),
        'history': history,
    }
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'已更新 index.json，歷史共 {len(history)} 天')

if __name__ == '__main__':
    main()
