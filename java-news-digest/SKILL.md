---
name: java-news-digest
description: 掃描 Java 相關新聞網站，依使用者指定的時間區間（如「上禮拜」、「本週」、「上個月」）抓取 Java、Spring、JVM 生態系的最新文章，整理重點摘要並翻譯成繁體中文，附上原始連結，輸出為 .md 檔案。**僅在使用者明確提到 Java、JVM、Spring、JEP、Kotlin（JVM 生態）等相關詞時觸發；若使用者說「所有技術新聞」或未指定語言，請勿觸發（應由 weekly-tech-digest 處理）。** 當使用者說「幫我看 Java 新聞」、「上禮拜有什麼 Java 動態」、「整理一下 Java 週報」、「Java 最新消息」、「JVM 新聞摘要」、「java news」、「幫我整理 Java 新聞」、「Java 新聞」、「上週的 Java 消息」、「最近 Java 有什麼新東西」時立即啟用。
---

# Java News Digest

你的任務是從指定的 Java 相關網站抓取新聞，依照使用者給定的時間區間過濾，整理並翻譯成繁體中文摘要，輸出為 .md 檔案。

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

用 WebFetch 依下列優先順序抓取每個網站：

### 第一優先：官方 / 權威來源
1. `https://inside.java` — Oracle 官方 Java 新聞
2. `https://openjdk.org/jeps/` — OpenJDK JEP 提案列表

### 第二優先：Newsletter
3. `https://www.baeldung.com/java-weekly` — Baeldung 週報（備用策略見下方）
4. `https://spring.io/blog.atom` — Spring 官方 Blog（用 atom feed 比直接抓網頁更可靠）

### 第三優先：社群 / 技術文章
5. `https://www.infoq.com/java/` — InfoQ Java
6. `https://www.baeldung.com/category/java/` — Baeldung 教學
7. `https://dzone.com/java-jdk-development-tutorials-tools-news` — DZone（備用策略見下方）

### 第四優先：討論區
8. `https://dev.to/t/java` — dev.to Java

**抓取策略：**
- 先 WebFetch 列表頁，從中找出發布日期在目標時間區間內的文章
- 若列表頁沒有完整摘要，再 WebFetch 個別文章（每個網站最多抓 5 篇全文，避免過多請求）
- 若某網站無法存取，立即嘗試備用策略（見下方），而非直接標記失敗

---

### Baeldung Java Weekly 說明

Baeldung Java Weekly 需要訂閱登入，**無法自動抓取**，請在輸出的 .md 檔案末尾加上以下提醒，讓使用者自行補充：

```
## 待手動補充

### Baeldung Java Weekly
> 需訂閱登入，請至 https://www.baeldung.com/java-weekly 自行查閱本期內容並補充。
```

---

### DZone 備用抓取策略

DZone 主分類頁常回 403，改用以下方法依序嘗試：

**方法 1：RSS Feed**
```
https://feeds.dzone.com/java
```

**方法 2：標籤頁**
```
https://dzone.com/tag/java
https://dzone.com/tag/jvm
https://dzone.com/tag/spring
```

**方法 3：Trending 頁（無需登入）**
```
https://dzone.com/articles?tag=java
```

若以上全部失敗，標記「本期無法存取」並繼續下一個來源。

## 步驟三：整理與翻譯

過濾掉廣告、招聘、純促銷文章，保留 Java、Spring、JVM 生態系相關內容。

### 文章數量 ≤ 10 篇的網站，每篇格式：

```
### [原文標題](原始連結)
**繁體中文標題翻譯**

- 重點一
- 重點二
- 重點三
（最多 5 個重點，聚焦技術亮點、版本變化、使用情境）
```

### 文章數量 > 10 篇的網站，只列標題與連結：

```
- [原文標題 — 繁體中文翻譯](原始連結)
```

**翻譯原則：**
- 使用繁體中文
- 技術術語保留英文（JEP、JDK、GC、Virtual Thread、Record 等）
- 重點簡潔有力，不需要翻譯原文每個字，抓住技術核心即可

## 步驟四：輸出檔案（.md 與 .docx 各一份）

**檔案命名前綴：** `java-news-YYYY-MM-DD_to_YYYY-MM-DD`
**存放路徑：** `~/data/create-data-from-claude/`

同一份內容輸出兩個格式：
1. `java-news-YYYY-MM-DD_to_YYYY-MM-DD.md` — Markdown 版
2. `java-news-YYYY-MM-DD_to_YYYY-MM-DD.docx` — Word 版

### 產生 .docx 的方式

用 Python + `python-docx` 套件根據整理好的內容產生 Word 檔，套用以下樣式：
- 文件標題（`Title` style）：「Java 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD」
- 大標（`Heading 1`）：官方 / 權威來源、Newsletter、社群 / 技術文章、討論區
- 中標（`Heading 2`）：各網站名稱（inside.java、Spring Blog 等）
- 文章標題（`Heading 3`）：每篇文章標題，後接超連結
- 重點條列（`List Bullet`）：各篇文章的重點 bullet points
- 「本週亮點 Top 5」區段放在最前面，條列格式

**產生 .docx 的 Python 範本程式碼：**

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
import re

doc = Document()

# 標題
doc.add_heading('Java 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD', 0)

# 中繼資訊（小字）
meta = doc.add_paragraph()
meta.add_run('整理時間：YYYY/MM/DD').font.size = Pt(10)

# 依序加入各區段...
# doc.add_heading('本週亮點 Top 5', level=1)
# doc.add_heading('官方 / 權威來源', level=1)
# doc.add_heading('inside.java', level=2)
# doc.add_heading('文章標題', level=3)
# doc.add_paragraph('重點一', style='List Bullet')

doc.save('/Users/alvinlo/data/create-data-from-claude/java-news-YYYY-MM-DD_to_YYYY-MM-DD.docx')
```

若系統未安裝 `python-docx`，先執行：`pip install python-docx`

完成後告知使用者兩個檔案的路徑。

### 輸出結構：

```markdown
# Java 新聞摘要：YYYY/MM/DD ~ YYYY/MM/DD

> 整理時間：YYYY/MM/DD
> 涵蓋來源：8 個網站

---

## 本週亮點 Top 5

從所有來源挑出最值得關注的 5 篇，每篇一句話說明為何重要。

1. [標題](連結) — 重要原因
2. ...

---

## 官方 / 權威來源

### inside.java（X 則）

...

### OpenJDK JEP（X 則）

...

---

## Newsletter

### Baeldung Java Weekly（X 則）

...

### Spring Blog（X 則）

...

---

## 社群 / 技術文章

### InfoQ Java（X 則）

...

### Baeldung（X 則）

...

### DZone（X 則）

...

---

## 討論區

### dev.to/java（X 則）

...
```

「本週亮點 Top 5」放在最前面，讓使用者快速掌握重點。
