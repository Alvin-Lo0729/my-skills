---
name: rust-news-digest
description: 掃描 Rust 程式語言相關新聞網站，依使用者指定的時間區間（如「上禮拜」、「本週」、「上個月」、「01/01~02/03」）抓取 Rust 生態系的最新文章，整理重點摘要並翻譯成繁體中文，附上原始連結，輸出為 .md 與 .docx 檔案。**僅在使用者明確提到 Rust、Cargo、crate、trait、async Rust 等 Rust 相關詞時觸發；若使用者說「所有技術新聞」或未指定語言，請勿觸發（應由 weekly-tech-digest 處理）。** 當使用者說「幫我看 Rust 新聞」、「上禮拜有什麼 Rust 動態」、「整理一下 Rust 週報」、「Rust 最新消息」、「Rust 新聞摘要」、「rust news」、「幫我整理 Rust 新聞」、「Rust 新聞」、「上週的 Rust 消息」、「最近 Rust 有什麼新東西」時立即啟用。
---

# Rust News Digest

你的任務是從指定的 Rust 相關網站抓取新聞，依照使用者給定的時間區間過濾，整理並翻譯成繁體中文摘要，同時輸出 .md 與 .docx 兩份檔案。

## 步驟一：確認時間範圍

將使用者的時間描述轉換為具體日期區間：

| 使用者說 | 轉換規則 |
|---------|---------|
| 「上禮拜」/「上週」 | 上一個完整週一 ~ 週日 |
| 「本週」 | 本週週一 ~ 今天 |
| 「最近 N 天」 | 今天往前 N 天 |
| 「上個月」 | 上一個完整月份 |
| 具體日期（如 01/01~02/03） | 直接使用，補上當前年份 |

開始前先說明：「抓取範圍：YYYY/MM/DD ~ YYYY/MM/DD」，讓使用者確認後再繼續。

## 步驟二：依優先順序抓取網站

用 WebFetch 依下列優先順序抓取每個網站：

### 第一優先：官方來源
1. `https://this-week-in-rust.org/` — This Week in Rust 週報（每週彙整最重要的社群資訊）
2. `https://blog.rust-lang.org/` — Rust 官方 Blog（版本公告、語言更新）

### 第二優先：技術文章聚合
3. `https://readrust.net/` — Read Rust（彙整各類 Rust 文章）
4. `https://rust.libhunt.com/newsletter` — Awesome Rust Newsletter

### 第三優先：語言設計討論
5. `https://internals.rust-lang.org/` — Rust Internals（RFC 與語言設計層面討論）

**抓取策略：**
- 先 WebFetch 列表頁，從中找出發布日期在目標時間區間內的文章
- 若列表頁沒有完整摘要，再 WebFetch 個別文章（每個網站最多抓 5 篇全文，避免過多請求）
- This Week in Rust 是週報格式，直接抓對應週次的頁面即可
- 若某網站無法存取，標記「本期無法存取」並繼續下一個來源

### This Week in Rust 抓取說明

This Week in Rust 每週一發布，URL 格式為：
```
https://this-week-in-rust.org/blog/YYYY/MM/DD/this-week-in-rust-NNN/
```
先抓首頁 `https://this-week-in-rust.org/` 找最新一期的連結，再根據時間區間決定要抓哪幾期。

## 步驟三：整理與翻譯

過濾掉廣告、招聘、純促銷文章，保留 Rust 生態系相關內容。

### 文章數量 ≤ 10 篇的網站，每篇格式：

```
### [原文標題](原始連結)
**繁體中文標題翻譯**

- 重點一
- 重點二
- 重點三
（3~5 個重點，聚焦技術亮點、版本變化、使用情境）
```

### 文章數量 > 10 篇的網站，只列標題與連結：

```
- [原文標題 — 繁體中文翻譯](原始連結)
```

**翻譯原則：**
- 使用繁體中文
- 技術術語保留英文（crate、trait、lifetime、borrow checker、async/await、unsafe、macro、RFC、WASM、Cargo 等）
- 重點簡潔有力，不需要翻譯原文每個字，抓住技術核心即可

## 步驟四：輸出檔案（.md 與 .docx 各一份）

**檔案命名前綴：** `rust-news-YYYY-MM-DD_to_YYYY-MM-DD`
**存放路徑：** `~/data/create-data-from-claude/`

同一份內容輸出兩個格式：
1. `rust-news-YYYY-MM-DD_to_YYYY-MM-DD.md` — Markdown 版
2. `rust-news-YYYY-MM-DD_to_YYYY-MM-DD.docx` — Word 版

### 產生 .docx 的方式

用 Python + `python-docx` 套件根據整理好的內容產生 Word 檔，套用以下樣式：
- 文件標題（`Title` style）：「Rust 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD」
- 大標（`Heading 1`）：官方來源、技術文章聚合、語言設計討論
- 中標（`Heading 2`）：各網站名稱
- 文章標題（`Heading 3`）：每篇文章標題，後接超連結
- 重點條列（`List Bullet`）：各篇文章的重點 bullet points
- 「本期亮點 Top 5」區段放在最前面，條列格式

**產生 .docx 的 Python 範本程式碼：**

```python
from docx import Document
from docx.shared import Pt
doc = Document()

# 標題
doc.add_heading('Rust 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD', 0)

# 中繼資訊（小字）
meta = doc.add_paragraph()
meta.add_run('整理時間：YYYY/MM/DD').font.size = Pt(10)

# 依序加入各區段...
# doc.add_heading('本期亮點 Top 5', level=1)
# doc.add_heading('官方來源', level=1)
# doc.add_heading('This Week in Rust', level=2)
# doc.add_heading('文章標題', level=3)
# doc.add_paragraph('重點一', style='List Bullet')

doc.save('/Users/alvinlo/data/create-data-from-claude/rust-news-YYYY-MM-DD_to_YYYY-MM-DD.docx')
```

若系統未安裝 `python-docx`，先執行：`pip install python-docx`

完成後告知使用者兩個檔案的路徑。

### 輸出結構：

```markdown
# Rust 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD

> 整理時間：YYYY/MM/DD
> 涵蓋來源：5 個網站

---

## 本期亮點 Top 5

從所有來源挑出最值得關注的 5 篇，每篇一句話說明為何重要。

1. [標題](連結) — 重要原因
2. ...

---

## 官方來源

### This Week in Rust（第 NNN 期）

...

### Rust Blog（X 則）

...

---

## 技術文章聚合

### Read Rust（X 則）

...

### Awesome Rust Newsletter（X 則）

...

---

## 語言設計討論

### Rust Internals（X 則）

...
```

「本期亮點 Top 5」放在最前面，讓使用者快速掌握重點。
