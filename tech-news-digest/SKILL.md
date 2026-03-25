---
name: tech-news-digest
description: 掃描資訊業相關新聞網站（Hacker News、Martin Fowler、The New Stack、High Scalability、iThome），依使用者指定的時間區間抓取後端、架構、雲端、AI 等領域的最新文章，整理重點摘要並翻譯成繁體中文，標題保留原文附翻譯，每篇 3~5 個重點，附原文連結，輸出為 .md 與 .docx 檔案。**僅在使用者明確提到「軟體業」、「後端」、「架構」、「Hacker News」、「iThome」等詞時觸發；若使用者說的是「Java 新聞」、「Rust 新聞」請勿觸發；若使用者說「所有技術新聞」、「資訊業新聞」或未指定領域請勿觸發（應由 weekly-tech-digest 處理）。** 當使用者說「幫我整理軟體業新聞」、「幫我看軟體業新聞」、「軟體業新聞摘要」、「幫我整理後端新聞」、「幫我看 Hacker News 整理」、「最近有什麼軟體業新聞」、「iThome 新聞整理」時立即啟用。
---

# Tech News Digest

你的任務是從指定的資訊業網站抓取新聞，依照使用者給定的時間區間過濾，整理並翻譯成繁體中文摘要，輸出為 .md 與 .docx 檔案。

## 步驟一：確認時間範圍

將使用者的時間描述轉換為具體日期區間：

| 使用者說 | 轉換規則 |
|---------|---------|
| 「上禮拜」/「上週」 | 上一個完整週一 ~ 週日 |
| 「本週」 | 本週週一 ~ 今天 |
| 「最近 N 天」 | 今天往前 N 天 |
| 「上個月」 | 上一個完整月份 |
| 具體日期 | 直接使用 |

開始前先說明：「抓取範圍：YYYY/MM/DD ~ YYYY/MM/DD」，讓使用者確認後再繼續。

## 步驟二：依優先順序抓取網站

用 WebFetch 依下列順序抓取每個網站：

### 1. Hacker News
URL：`https://news.ycombinator.com`

抓取策略：
- 先 WebFetch `https://news.ycombinator.com` 取得首頁熱門列表
- 篩選資訊業相關文章（後端、架構、雲端、AI、開發工具、系統設計等），排除純政治、財經、娛樂
- **前 5 篇熱門相關文章**：WebFetch 原文，整理 3~5 個重點摘要
- **其餘相關文章**：只保留標題與連結，不抓全文

### 2. The New Stack
URL：`https://thenewstack.io`

抓取策略：
- WebFetch 首頁或 `https://thenewstack.io/category/cloud-native/` 取得文章列表
- 找出發布日期在目標時間區間內的文章
- 每篇 WebFetch 全文，整理 3~5 個重點

### 3. High Scalability
URL：`http://highscalability.com`

抓取策略：
- WebFetch `http://highscalability.com/blog/` 取得文章列表
- 找出時間區間內的系統設計、架構案例文章
- 每篇整理 3~5 個重點，重點說明技術選型與規模

### 4. Martin Fowler
URL：`https://martinfowler.com`

抓取策略：
- WebFetch `https://martinfowler.com` 首頁
- 找出時間區間內的新文章或更新文章
- 文章量通常較少，有則全部整理，重點聚焦架構觀念與設計模式

### 5. iThome
URL：`https://www.ithome.com.tw`

抓取策略：
- WebFetch `https://www.ithome.com.tw` 首頁或 `https://www.ithome.com.tw/news` 取得列表
- 找出時間區間內的資訊業相關新聞（後端、雲端、AI、開發工具，排除純硬體、消費性電子）
- 每篇整理 3~5 個重點
- iThome 為中文內容，**標題與重點不需要翻譯**，格式與其他網站一致

### Architecture Weekly（手動補充）

Architecture Weekly 為訂閱制 Newsletter，**無法自動抓取**。
在輸出檔案末尾加上以下提醒：

```
## 待手動補充

### Architecture Weekly（by Oskar Dudycz）
> 訂閱制 Newsletter，請至信箱查閱本期內容並自行補充。
> 訂閱連結（如需）：https://www.architecture-weekly.com
```

## 步驟三：整理與翻譯

過濾廣告、招聘、純促銷文章，保留後端、架構、雲端、AI、系統設計、開發工具相關內容。

### 有全文的文章（每篇格式）：

```
### [原文標題](原始連結)
**繁體中文標題翻譯**

- 重點一
- 重點二
- 重點三
（3~5 個重點，聚焦技術亮點、架構觀念、使用情境）
```

### Hacker News 其餘文章（只列標題與連結）：

```
- [原文標題 — 繁體中文翻譯](原始連結)
```

### iThome 文章（中文，不需翻譯）：

```
### [新聞標題](原始連結)

- 重點一
- 重點二
- 重點三
```

**翻譯原則：**
- 使用繁體中文
- 專有名詞保留英文（Kubernetes、Docker、LLM、RAG、gRPC、WebAssembly、CI/CD 等）
- 重點簡潔，抓住技術核心即可，不需逐字翻譯

## 步驟四：輸出檔案（.md 與 .docx 各一份）

**檔案命名前綴：** `tech-news-YYYY-MM-DD_to_YYYY-MM-DD`
**存放路徑：** `~/data/create-data-from-claude/`

### .md 輸出結構：

```markdown
# 資訊業新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD

> 整理時間：YYYY/MM/DD
> 涵蓋來源：Hacker News、The New Stack、High Scalability、Martin Fowler、iThome

---

## 本期亮點 Top 10

從所有來源挑出最值得關注的文章（若總數不足 10 篇則依實際數量列出），每篇一句話說明為何重要。

1. [標題](連結) — 重要原因
2. ...

---

## Hacker News

### 精選全文（前 5 篇）

...（標題 + 重點）

### 其他相關文章

- [標題 — 中文翻譯](連結)
- ...

---

## The New Stack（X 則）

...

---

## High Scalability（X 則）

...

---

## Martin Fowler（X 則）

...

---

## iThome（X 則）

...

---

## 待手動補充

### Architecture Weekly（by Oskar Dudycz）
> 訂閱制 Newsletter，請至信箱查閱本期內容並自行補充。
```

### 產生 .docx 的方式

用 Python + `python-docx` 套件根據整理好的內容產生 Word 檔：

```python
from docx import Document
from docx.shared import Pt

doc = Document()

# 文件標題
doc.add_heading('資訊業新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD', 0)

meta = doc.add_paragraph()
meta.add_run('整理時間：YYYY/MM/DD').font.size = Pt(10)

# 依序加入各區段
# doc.add_heading('本期亮點 Top 10', level=1)
# doc.add_heading('Hacker News', level=1)
# doc.add_heading('精選全文（前 5 篇）', level=2)
# doc.add_heading('文章標題', level=3)
# doc.add_paragraph('重點一', style='List Bullet')
# doc.add_heading('其他相關文章', level=2)
# doc.add_paragraph('標題 — 中文翻譯  連結', style='List Bullet')

doc.save('/Users/alvinlo/data/create-data-from-claude/tech-news-YYYY-MM-DD_to_YYYY-MM-DD.docx')
```

docx 結構：
- `Title` style：文件標題
- `Heading 1`：各網站名稱（Hacker News、The New Stack 等）
- `Heading 2`：子分類（精選全文、其他相關文章）
- `Heading 3`：每篇文章標題（後接超連結）
- `List Bullet`：重點條列
- 「本期亮點 Top 10」區段放在最前面

若系統未安裝 `python-docx`，先執行：`pip install python-docx`

完成後告知使用者兩個檔案的完整路徑。
