---
name: anki-word-importer
description: >
  Anki 英文單字卡製作工具。當使用者想把英文單字加入 Anki、製作單字卡、查字典後匯出到 Anki，
  或說「幫我加 XXX 到 Anki」、「查 XXX 並生成 Anki 卡片」、「我要複習這個單字」時立即啟用。
  此 skill 會自動從 Oxford 抓音標與發音，從劍橋字典抓中英文意思與範例，
  並輸出可直接匯入 Anki 的 TSV 檔案，不需要使用者手動輸入任何資料。
---

# Anki 英文單字匯入工具

幫使用者完全自動化以下流程：
1. 先從 Cambridge Dictionary（英中版）取得所有意思（英文 + 中文 + 英文範例），同時取得 Cambridge 重新導向後的**標準字形**（例如輸入 activities → Cambridge 找到 activity）
2. 用標準字形去 Oxford Learner's Dictionary 取得音標和 UK 發音 MP3（避免複數/過去式找不到音檔）
3. 生成可匯入 Anki 的 TSV 格式，輸出到 `~/anki-import-file/`

## 使用流程

### Step 1：確認輸入

只需要單字名稱即可，**不需要指定詞性**。腳本會自動從 Cambridge 抓取所有詞性。

若使用者一次給多個單字（如「run book happy」），逐一處理。

### Step 2：執行腳本

對每個單字執行：

```bash
python3 /Users/alvinlo/.claude/skills/anki-word-importer/scripts/fetch_word.py <word>
```

- 如果一次處理多個單字，每個之間等 2 秒避免被封鎖

### Step 3：展示結果

執行完畢後，簡短告知使用者：
- 音標是什麼
- 取得了幾個意思，合併為 1 個檔案
- 檔案存到哪裡（格式：`~/anki-import-file/<word>.txt`）

**失敗時的回報方式：**

根據腳本的 exit code 和 stderr 輸出判斷失敗原因，並明確告知使用者：

| 失敗情況 | 回報訊息格式 |
|----------|--------------|
| Cambridge 找不到「{單字}」的任何意思 | ❌ `{單字}`：找不到字典資料，請確認拼字是否正確 |
| Oxford 音標未取得 | ⚠️ `{單字}`：音標未取得（其他資料正常） |
| 音檔下載失敗 | ⚠️ `{單字}`：音檔下載失敗（其他資料正常） |
| 網路錯誤 / 網站封鎖 | ❌ `{單字}`：網路存取失敗，建議稍後再試 |

每個失敗都要明確寫出**是哪個單字**發生問題。

### Step 4：Anki 匯入說明（第一次使用時說明）

```
Anki 匯入步驟：
1. 開啟 Anki → 檔案 → 匯入（File → Import）
2. 選擇 ~/anki-import-file/<word>.txt（一個單字一個檔案，檔案內每行為一個意思）
3. 確認欄位對應：單字 / 音標 / 詞性 / 英文解釋 / 中文解釋 / 範例
4. 將 ~/anki-import-file/<word>__gb_1.mp3 複製到 Anki 媒體資料夾
   （在 Anki 中：工具 → 檢查媒體檔案，可看到媒體資料夾位置）
```

## 輸出格式說明

生成的 TSV 格式（Anki Basic 牌型）：

**正面（Front）：**
```
run  /rʌn/  [sound:run__gb_1.mp3]
```

**背面（Back）：**
```
1. (of people and some animals) to move along, faster than walking...
▶ 跑，奔跑
"I can run a mile in five minutes."

────────────────────────────────
2. If you run an animal in a race, you cause it to take part.
▶ 使（狗、馬等）參加比賽
"Thompson Stables are running three horses in the next race."
```

## 常見問題處理

| 狀況 | 處理方式 |
|------|----------|
| 音標抓不到 | 只放音檔連結，音標欄位留空 |
| 音檔下載失敗 | 告訴使用者手動下載 URL，跳過 [sound:] 標記 |
| Cambridge 找不到意思 | 提示可能是詞性錯誤，建議換詞性再試 |
| 網站暫時封鎖 | 建議稍後再試，或嘗試 VPN |

## 多個單字一次處理

使用者可以一次輸入多個單字，例如：
- 「幫我加 run(動詞)、book(名詞)、happy(形容詞) 到 Anki」

這時，依序執行每個單字的腳本，**即使中途有失敗也要繼續處理其他單字**。

最後統一回報結果，格式如下：

```
✅ 成功（3 個）：run、book、happy
❌ 失敗（1 個）：
  • xyzabc：找不到字典資料，請確認拼字是否正確
```

若全部成功，只需顯示成功清單即可，不需要顯示失敗區塊。
