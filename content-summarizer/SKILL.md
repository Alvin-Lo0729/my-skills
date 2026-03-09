---
name: content-summarizer
description: >
  將影片、網站或文字內容整理成結構化的繁體中文 Word 重點摘要檔案。
  當使用者提供 YouTube 連結、其他影音網站連結、本地影片檔案路徑、網站 URL，
  或貼上大量文字，並希望整理重點、歸納摘要、做筆記時，立即使用此 skill。
  即使使用者沒有明確說「摘要」或「整理」，只要他們分享內容並想「了解重點」、
  「幫我看一下」、「整理一下」、「做成筆記」，都應該觸發此 skill。
  輸出格式固定為 .docx Word 檔案，包含標題、摘要與詳細條列重點。
---

# Content Summarizer

將任何內容（影片、網站、文字）整理成結構清晰的繁體中文 Word 重點摘要。

## 輸入類型判斷

根據使用者提供的內容決定處理方式：

| 輸入類型 | 判斷方式 | 處理方法 |
|---------|---------|---------|
| YouTube 連結 | URL 含 `youtube.com` 或 `youtu.be` | 用 `yt-dlp` 抓字幕 |
| 其他影音網站 | URL 來自 Bilibili、Vimeo、TED 等 | 用 `yt-dlp` 嘗試抓字幕 |
| 本地影片檔 | 使用者提供本地路徑（.mp4/.mkv/.mov 等） | ffmpeg + whisper 轉錄 |
| 網站 URL | http/https 連結但非影音 | WebFetch 抓網頁內容 |
| 純文字 | 使用者直接貼上文字 | 直接處理 |

## 處理流程

### Step 1：取得原始內容

**YouTube / 其他影音網站：**
```bash
# 先嘗試抓字幕（最快）
yt-dlp --skip-download --write-subs --write-auto-subs \
  --sub-lang zh-Hant,zh-Hans,zh,en \
  --sub-format vtt --convert-subs srt \
  -o "/tmp/transcript_%(id)s" "<URL>"

# 如果沒有字幕，改抓音訊再 whisper 轉錄
yt-dlp -x --audio-format mp3 -o "/tmp/audio_%(id)s.%(ext)s" "<URL>"
```

**本地影片檔案：**
```bash
# 先用 ffmpeg 抽出音訊
ffmpeg -i "<video_path>" -vn -acodec mp3 /tmp/audio_local.mp3

# 再用 whisper 轉錄
whisper /tmp/audio_local.mp3 --language auto --output_format txt --output_dir /tmp/
```

**注意事項：**
- 如果 `yt-dlp` 或 `whisper` 未安裝，告知使用者需要安裝（`brew install yt-dlp`、`pip install openai-whisper`）
- 如果字幕是 SRT 格式，先清理時間碼後再處理
- Whisper 轉錄時間較長，告知使用者需等待

**網站 URL：**
使用 WebFetch 工具抓取頁面內容，移除導航、廣告等雜訊，保留主要正文。

**純文字：**
直接使用使用者貼上的文字。

### Step 2：整理與歸納

拿到原始文字後，進行以下歸納：

1. **理解整體結構**：先瀏覽全文，掌握主題、脈絡與重要概念
2. **提取核心重點**：找出 5-10 個最重要的論點或資訊
3. **組織邏輯順序**：讓重點有因果或遞進關係，不是隨機條列
4. **加入補充說明**：每個重點下方加入 1-3 個子項目，說明細節、例子或佐證
5. **處理語言**：
   - 全文用繁體中文撰寫
   - 專有名詞保留原文（如：Machine Learning、API、ChatGPT）
   - 不好翻譯的術語直接用原文，括號內可加說明

### Step 3：建立 Word 檔案

使用 `scripts/create_docx.py` 產生格式化的 Word 文件：

```bash
python /Users/alvinlo/.claude/skills/content-summarizer/scripts/create_docx.py \
  --title "<標題>" \
  --summary "<摘要文字>" \
  --points "<JSON格式的重點陣列>" \
  --output "<輸出路徑>"
```

或者直接用 Python 呼叫，詳見腳本說明。

## Word 文件格式

```
[標題]                          ← 粗體大字，置中
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
來源：[URL 或檔案名稱]           ← 灰色小字
整理日期：[日期]

【摘要】
[2-4 句話的整體摘要，讓讀者快速掌握主旨]

【重點整理】
1. [重點標題]
   • [補充說明或細節]
   • [具體例子或數據]

2. [重點標題]
   • [補充說明]
   ...
```

**格式規則：**
- 標題：置中、粗體、20pt
- 「摘要」「重點整理」段落標題：粗體、14pt
- 重點編號項目：粗體、12pt
- 子項目說明：一般、11pt、縮排
- 全文字型：新細明體（或 Microsoft JhengHei）

## 輸出位置

預設儲存到使用者桌面或當前工作目錄，命名格式：
`[YYYY-MM-DD]_[標題前15字].docx`

完成後告知使用者檔案位置，並在對話中顯示摘要預覽。

## 錯誤處理

- **無法取得字幕且無 whisper**：告知限制，詢問使用者是否能提供文字逐字稿
- **網站需要登入**：提示無法抓取，請使用者複製貼上文字
- **影片太長（>2 小時）**：告知轉錄時間可能較長，詢問是否繼續
- **python-docx 未安裝**：提示 `pip install python-docx` 後重試
