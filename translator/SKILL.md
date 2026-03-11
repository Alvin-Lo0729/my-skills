---
name: translator
description: >
  將英文或日文內容翻譯成繁體中文，輸出雙語對照檔案（預設 Word .docx）。
  當使用者說「幫我翻譯」、「translate this」、「這段英文/日文翻成中文」、
  「翻一下這個檔案」、「把這段翻譯給我」、「幫我看這篇文章」並附上外文內容，
  或貼上英文/日文文字並希望看懂內容時，立即使用此 skill。
  即使使用者沒有說「翻譯」，只要他們貼上外文並問「這是什麼意思」、「幫我看懂」，也應觸發。
  輸出預設為 .docx 雙語對照，也支援 .txt、.md、.pdf。
---

# Translator

將英文或日文翻譯成繁體中文，輸出雙語對照文件。

## 輸入來源判斷

| 輸入類型 | 判斷方式 | 處理方法 |
|---------|---------|---------|
| 貼上文字 | 使用者直接在對話框輸入外文 | 直接翻譯 |
| txt 檔 | 路徑以 `.txt` 結尾 | Read 工具讀取 |
| pdf 檔 | 路徑以 `.pdf` 結尾 | Read 工具讀取 |
| docx 檔 | 路徘以 `.docx` 結尾 | 用 `python-docx` 讀取文字 |

如果使用者沒有指定輸出格式，**預設輸出 .docx**。

## 翻譯原則

1. **目標語言**：繁體中文
2. **專有名詞**：保留原文，不強行翻譯。例如：
   - 品牌名稱：Apple、Tesla、Toyota 保留
   - 技術術語：API、Machine Learning、Docker 保留
   - 人名地名：可酌情保留原文
   - 如果原文已有通用中文譯名（如 "artificial intelligence" → 人工智慧），可使用
3. **語氣**：保持原文語氣（正式/非正式、技術性/口語）
4. **段落結構**：保持與原文相同的段落分割，不要合併或拆分

## 翻譯流程

### Step 1：讀取原文

- 貼上文字：直接使用
- 檔案：用對應工具讀取內容
- 如果是 `.docx`，執行：
  ```bash
  python3 -c "
  from docx import Document
  doc = Document('<path>')
  for para in doc.paragraphs:
      print(para.text)
  "
  ```

### Step 2：翻譯

逐段翻譯，注意：
- 保持原文段落結構（一段原文對一段譯文）
- 遇到專有名詞直接保留原文
- 翻譯完成後確認語意是否通順自然

### Step 3：輸出檔案

**確認輸出路徑**：
- 使用者有指定路徑 → 使用指定路徑
- 未指定 → 預設存到桌面：`~/Desktop/`
- 檔名格式：`[YYYY-MM-DD]_translation_[標題前15字].[副檔名]`

根據輸出格式呼叫對應方式：

**Word (.docx) — 預設：**
```bash
python3 /Users/alvinlo/.claude/skills/translator/scripts/create_translation_docx.py \
  --title "<文件標題>" \
  --segments '<JSON格式的段落陣列>' \
  --source "<來源說明>" \
  --output "<輸出路徑>"
```

segments 格式：
```json
[
  {"original": "原文段落1", "translation": "譯文段落1"},
  {"original": "原文段落2", "translation": "譯文段落2"}
]
```

**Markdown (.md)：**
直接用 Write 工具輸出，格式見下方。

**純文字 (.txt)：**
直接用 Write 工具輸出，格式見下方。

**PDF (.pdf)：**
先產出 .md 檔案，再嘗試用以下方式轉換：
```bash
# 方法1：pandoc（如已安裝）
pandoc "<input.md>" -o "<output.pdf>" --pdf-engine=xelatex -V CJKmainfont="PingFang TC"

# 方法2：如果 pandoc 不可用，告知使用者開啟 .docx 後另存為 PDF
```

## 輸出格式範例

### Word / Markdown / txt 共用結構

```
標題：[文件標題]
來源：[來源說明]
翻譯日期：[日期]
━━━━━━━━━━━━━━━━━━━━━━━

【原文】
[第一段原文]

【譯文】
[第一段譯文]

─────────────────────

【原文】
[第二段原文]

【譯文】
[第二段譯文]
```

Markdown 使用 `**原文**` / `**譯文**` 標題格式，並在段落之間加 `---` 分隔線。

## 完成後

告知使用者：
1. 檔案已儲存的路徑
2. 在對話中顯示前 1-2 段的翻譯預覽，讓使用者確認翻譯品質
3. 如果有遇到不確定的專有名詞或語意模糊處，主動說明

## 錯誤處理

- **python-docx 未安裝**：提示 `pip install python-docx` 後重試
- **PDF 轉換工具不存在**：先輸出 .docx，告知使用者手動另存為 PDF
- **檔案路徑不存在**：告知使用者並請確認路徑
- **pandoc 未安裝**：`brew install pandoc`
