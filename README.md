# 公司資料異動查詢

每日自動從經濟部商業署 Open Data API 抓取公司異動資料，儲存為 JSON，並以靜態網頁展示。

## 架構

```
GitHub Actions (每天早上 9:00 台灣時間)
  └─ 執行 scripts/fetch.py
       └─ 呼叫 data.gcis.nat.gov.tw API
       └─ 儲存 data/YYYYMMDD.json
       └─ 更新 data/index.json
GitHub Pages
  └─ 展示 index.html（讀取 data/*.json）
```

## 快速開始

### 步驟 1：Fork 或建立 Repository

在 GitHub 建立一個新的 repository，並把以下檔案上傳：

```
.github/workflows/fetch-data.yml
scripts/fetch.py
index.html
data/          ← 建立空資料夾（放一個 .gitkeep 檔即可）
```

### 步驟 2：啟用 GitHub Pages

1. 進入 repository → Settings → Pages
2. Source 選 **GitHub Actions** 或 **Deploy from a branch → main / root**
3. 儲存後，幾分鐘內網頁就上線了

### 步驟 3：手動觸發第一次抓取

1. 進入 repository → Actions → 「每日抓取公司異動資料」
2. 點選「Run workflow」→「Run workflow」
3. 等約 1 分鐘，Actions 完成後 `data/` 資料夾會出現 JSON 檔

### 步驟 4：確認網頁正常

進入你的 GitHub Pages 網址（格式：`https://你的帳號.github.io/repo名稱/`）即可使用。

## 自動排程

`.github/workflows/fetch-data.yml` 設定為每天 UTC 01:00（台灣時間 09:00）自動執行。
可修改 cron 時間調整排程。

## 資料說明

- API 來源：[經濟部商業署公司資料異動查詢](https://data.gcis.nat.gov.tw)
- 授權：政府資料開放授權條款 第1版
- 每次最多抓取 1000 筆異動記錄
- 歷史資料保留最近 30 天
