---
name: weekly-tech-digest
description: 整合 Java、Rust、資訊業（Hacker News、iThome 等）三個領域的技術新聞，用 sub-agent 並行抓取，合併輸出單一 .md 摘要檔案。當使用者說「整理上禮拜新聞」、「幫我看這週技術新聞」、「本週技術週報」、「所有技術新聞」、「技術動態整理」、「weekly news」、「新聞整理」（未指定特定語言或領域）時立即啟用。即使使用者只說「上禮拜有什麼新聞」、「最近技術動態」、「幫我整理新聞」也應觸發。若使用者明確說「只要 Java」或「只要 Rust」，則分別交給 java-news-digest 或 rust-news-digest 處理，不觸發此 skill。
---

# Weekly Tech Digest

你的任務是用 **sub-agent 並行** 抓取 Java、Rust、資訊業三個領域的技術新聞，整理後合併輸出單一 `.md` 檔案。

## 步驟一：確認時間範圍與領域

將使用者的時間描述轉換為具體日期區間：

| 使用者說 | 轉換規則 |
|---------|---------|
| 「上禮拜」/「上週」 | 上一個完整週一 ~ 週日 |
| 「本週」 | 本週週一 ~ 今天 |
| 「最近 N 天」 | 今天往前 N 天 |
| 「上個月」 | 上一個完整月份 |
| 具體日期 | 直接使用 |

確認後說明：「抓取範圍：YYYY/MM/DD ~ YYYY/MM/DD，將並行抓取 Java、Rust、資訊業三個領域。」

預設抓取全部三個領域。若使用者有指定（如「這次不要 Rust」），則跳過對應領域。

## 步驟二：用 sub-agent 並行抓取三個領域

**同時** 啟動三個 sub-agent，每個負責一個領域。不要循序執行——三個一起跑，才能縮短總時間。

---

### Sub-agent A：資訊業新聞（Hacker News、The New Stack 等）

抓取以下網站，時間區間內的文章：

1. `https://news.ycombinator.com` — Hacker News
   - 抓首頁熱門列表，篩選後端、架構、雲端、AI、開發工具相關（排除政治、財經、娛樂）
   - 前 5 篇熱門相關文章：WebFetch 原文，整理 3~5 個重點
   - 其餘相關文章：只保留標題與連結

2. `https://thenewstack.io` — The New Stack
   - WebFetch 首頁，找時間區間內的文章
   - 每篇整理 3~5 個重點

3. `http://highscalability.com/blog/` — High Scalability
   - 找時間區間內的系統設計、架構案例文章
   - 每篇整理 3~5 個重點，重點說明技術選型與規模

4. `https://martinfowler.com` — Martin Fowler
   - 找時間區間內的新文章或更新
   - 聚焦架構觀念與設計模式

5. `https://www.ithome.com.tw/news` — iThome
   - 找時間區間內的資訊業相關新聞（排除純硬體、消費性電子）
   - iThome 為中文，不需翻譯

若某網站無法存取，標記「本期無法存取」繼續下一個。

**輸出格式（回傳給主 agent）：**
```
## 資訊業新聞

### Hacker News
#### 精選全文（前 5 篇）
### [原文標題](連結)
**繁體中文標題**
- 重點一
- 重點二

#### 其他相關文章
- [原文標題 — 中文翻譯](連結)

### The New Stack（X 則）
...

### High Scalability（X 則）
...

### Martin Fowler（X 則）
...

### iThome（X 則）
...
```

---

### Sub-agent B：Java 新聞

抓取以下網站，時間區間內的文章：

1. `https://inside.java` — Oracle 官方 Java 新聞
2. `https://openjdk.org/jeps/` — OpenJDK JEP 提案
3. `https://spring.io/blog.atom` — Spring 官方 Blog（atom feed）
4. `https://www.infoq.com/java/` — InfoQ Java
5. `https://www.baeldung.com/category/java/` — Baeldung 教學
6. `https://dev.to/t/java` — dev.to Java
7. DZone（若主頁 403，嘗試 `https://feeds.dzone.com/java` 或 `https://dzone.com/tag/java`）

每個網站最多抓 5 篇全文，文章數 > 10 篇時只列標題與連結。

注意：Baeldung Java Weekly 需登入，無法自動抓取，在輸出末尾加上「待手動補充」提醒。

**輸出格式（回傳給主 agent）：**
```
## Java 新聞

### inside.java（X 則）
### [原文標題](連結)
**繁體中文標題**
- 重點一
- 重點二

### Spring Blog（X 則）
...

### 待手動補充
> Baeldung Java Weekly 需登入，請至 https://www.baeldung.com/java-weekly 自行補充。
```

---

### Sub-agent C：Rust 新聞

抓取以下網站，時間區間內的文章：

1. `https://this-week-in-rust.org/` — This Week in Rust 週報
   - 先抓首頁找最新一期連結，再根據時間區間抓對應期次
2. `https://blog.rust-lang.org/` — Rust 官方 Blog
3. `https://readrust.net/` — Read Rust
4. `https://rust.libhunt.com/newsletter` — Awesome Rust Newsletter
5. `https://internals.rust-lang.org/` — Rust Internals（RFC 與語言設計討論）

每個網站最多抓 5 篇全文，文章數 > 10 篇時只列標題與連結。

**輸出格式（回傳給主 agent）：**
```
## Rust 新聞

### This Week in Rust（第 NNN 期）
### [原文標題](連結)
**繁體中文標題**
- 重點一
- 重點二

### Rust Blog（X 則）
...
```

---

## 步驟三：等待三個 sub-agent 完成，合併結果

收到三個 sub-agent 的結果後，合併成一份完整摘要。

### 翻譯原則（適用所有領域）
- 使用繁體中文
- 技術術語保留英文（Kubernetes、Docker、JEP、Virtual Thread、crate、trait、async/await、RFC、WASM 等）
- 重點簡潔，抓技術核心，不需逐字翻譯
- iThome 為中文，不需翻譯

## 步驟四：輸出 .md 檔案

**檔案命名：** `weekly-tech-digest-YYYY-MM-DD_to_YYYY-MM-DD.md`
**存放路徑：** `~/data/create-data-from-claude/`

### 輸出結構：

```markdown
# 技術週報：YYYY/MM/DD ~ YYYY/MM/DD

> 整理時間：YYYY/MM/DD
> 涵蓋領域：資訊業（Hacker News、The New Stack、High Scalability、Martin Fowler、iThome）、Java、Rust

---

## 本期亮點 Top 10

從所有領域挑出最值得關注的文章，每篇一句話說明為何重要。

1. [標題](連結) — 重要原因（領域標籤：Java / Rust / 資訊業）
2. ...

---

## 資訊業新聞

（Sub-agent A 的結果）

---

## Java 新聞

（Sub-agent B 的結果）

---

## Rust 新聞

（Sub-agent C 的結果）

---

## 待手動補充

### Architecture Weekly（by Oskar Dudycz）
> 訂閱制 Newsletter，請至信箱查閱本期內容並自行補充。

### Baeldung Java Weekly
> 需登入，請至 https://www.baeldung.com/java-weekly 自行補充。
```

完成後告知使用者檔案路徑，說明哪些領域成功抓取、哪些網站無法存取、哪些需手動補充。
