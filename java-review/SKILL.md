---
name: java-review
description: >
  針對 Java 專案的完整 code review 工作流，包含 Sub-agent 探索、Context 管理、
  以及 PR Mental Alignment（將 AI 操作脈絡附在 PR 中讓 reviewer 理解）。
  當使用者提到要 review Java 程式碼、找 bug、審查 PR、重構某個模組、
  檢查效能或安全性問題、或想把 AI 操作過程整合進 PR 描述時，立即啟用此 skill。
  即使使用者只說「幫我看這段 Java」、「這個 PR 可以 review 嗎」、「review 一下這個類別」也應觸發。
  本 skill 強制三個階段：Research → Plan → Implement，每個階段均需人工確認，
  並在 PR 階段產出 AI 操作脈絡文件，讓 reviewer 能讀計畫而非只看 green diff。
---

# Java Review — Context-Aware Code Review

基於「No Vibes Allowed」方法論（Dex Horthy），核心信念：
**context 品質決定輸出品質。垃圾進、垃圾出。**

不急著動手 → 先理解 → 再計畫 → 最後才實作。

---

## Phase 1：Research（理解系統）

**目標：** 在不修改任何程式碼的前提下，建立對問題範圍的完整理解。

### 步驟一：評估探索規模

| 情境 | 執行方式 |
|------|----------|
| 使用者直接貼上程式碼 | 直接分析，無需 sub-agent |
| 指定 1–2 個明確檔案 | 直接讀取，無需 sub-agent |
| 只有類別名稱 / 功能描述，需在 codebase 尋找 | **啟動 Explorer Sub-agent** |
| 涉及 3+ 個相互依賴的模組 | **啟動 Explorer Sub-agent** |

### 步驟二A：直接分析（小範圍）

1. 讀取目標類別
2. 讀取它依賴的介面與關鍵實作
3. 找出呼叫它的上層程式碼（caller）
4. 找出對應的測試檔案
5. 從命名、註解、測試推斷設計意圖

### 步驟二B：啟動 Explorer Sub-agent（大範圍）

讀取 `agents/explorer.md`，依照其指令啟動 sub-agent。

Sub-agent 回傳後：
- **只讀取** sub-agent 指出的精確檔案與行號
- **不重複搜尋** 整個 codebase
- 保持 parent context 乾淨

### 步驟三：輸出 Research 文件

在對話中顯示以下格式，**並儲存**為 `.ai-review/YYYY-MM-DD_research_[描述].md`：

```
## Research 結果

### 涉及範圍
- `src/main/java/.../Foo.java` — 主要目標，負責 [描述]
- `src/main/java/.../Bar.java` — 被 Foo 依賴，[描述]
- `src/test/java/.../FooTest.java` — 測試覆蓋 [描述]

### 架構摘要
[2–5 句話描述目前的設計，包含資料流方向]

### 發現的潛在問題
- [問題A]（位置：Foo.java:42）
- [問題B]（位置：Bar.java:87–103）
```

**暫停，詢問使用者：**
> 「Research 完成。以上理解是否正確？有沒有遺漏的脈絡或背景知識？確認後我將進入 Plan 階段。」

---

## Phase 2：Plan（計畫）

**目標：** 產出詳細計畫，讓使用者在不執行程式碼的情況下能完整理解所有變更。

### Plan 必須包含

**1. 審查結論（四個面向）**

針對以下面向逐一說明問題與嚴重程度：
- **邏輯正確性（Logic）**：NPE、例外處理、邊界條件
- **效能（Performance）**：N+1 查詢、不必要的 autoboxing、Stream 效率
- **安全性（Security）**：SQL injection、反序列化、敏感資料洩漏
- **程式碼風格（Style）**：命名、SRP、DRY、方法長度

**2. 變更步驟（逐步說明）**

每個步驟包含：
- 要修改的檔案與精確行號
- 修改前的程式碼片段
- 修改後的程式碼片段
- 解釋「為什麼這樣改」

**3. 測試計畫**

- 要執行的既有測試
- 需要新增的測試案例及原因

### Plan 輸出格式

````markdown
## Code Review Plan

### 審查結論

**邏輯正確性**
- ⚠️ [問題描述] — `Foo.java:42`
  > 原因：[解釋]

**效能**
- ⚠️ [問題描述] — `Bar.java:87`
  > 原因：[解釋]

**安全性**
- ✅ 未發現明顯安全疑慮

**程式碼風格**
- 💡 [建議] — `Foo.java:15–20`

---

### 變更步驟

#### 步驟 1：[目的]
檔案：`src/.../Foo.java`，第 42 行

**修改前：**
```java
// 原始程式碼
```

**修改後：**
```java
// 改動後的程式碼
```

原因：[為什麼這樣改更好]

---

### 測試計畫
- 執行 `FooTest#testXxx()` 確認邏輯正確
- 新增測試：[描述]
````

### 儲存 Plan 檔案

儲存到 `.ai-review/YYYY-MM-DD_plan_[描述].md`
（若 `.ai-review/` 目錄不存在則建立）

### 強制暫停

> 「計畫已準備好，請 review 以上內容。確認後說「開始實作」，或告訴我需要調整的地方。」

**不得在使用者明確確認前進入 Phase 3。**

---

## Phase 3：Implement（實作）

**目標：** 按照確認後的計畫逐步執行，每步驟後驗證。

### 執行原則

- **逐步執行** — 完成一個步驟後確認無誤再進行下一步
- **不偏離計畫** — 發現計畫有誤時，暫停說明，不自行決定
- **Context 紀律** — 每個步驟只讀取當前需要的檔案
- **不過度修改** — 只改計畫中列出的部分，不「順便」修改其他地方

### 實作完成後輸出摘要

```
## 實作摘要

### 已完成的變更
- `Foo.java:42` — [描述]
- `Bar.java:87–103` — [描述]

### 測試結果
- [測試名稱]：✅ 通過 / ❌ 失敗（附說明）

### 未處理但建議追蹤的問題
- [若有發現但本次未修改的問題，列在這裡]
```

**實作完成後，詢問使用者：**
> 「實作已完成。是否需要產出 PR Mental Alignment 文件？這份文件可以附在 Pull Request 中，讓 reviewer 了解 AI 的完整操作脈絡。」

---

## PR Mental Alignment（AI 脈絡同步）

### 為什麼需要這個？

當 AI 產出 2–3 倍程式碼時，reviewer 只看 green diff 根本無法理解來龍去脈。
**閱讀「計畫文件」是技術領導者維持共同理解的有效方式。**

reviewer 需要看到：使用者的原始需求 → AI 的研究發現 → 決策理由 → 實際變更 → 測試結果

### 產出 PR Mental Alignment 文件

儲存到 `.ai-review/YYYY-MM-DD_pr-context_[描述].md`，格式如下：

````markdown
## PR: [PR 標題]

> 此文件由 AI 輔助產出，記錄本次 code review 與修改的完整脈絡，
> 供 reviewer 在看 diff 前先建立背景理解。

---

### 需求背景
[使用者原始描述的問題或需求，保留原話]

---

### Research 發現
**涉及範圍：**
- `Foo.java` — [職責描述]
- `Bar.java` — [職責描述]

**架構摘要：**
[2–3 句話描述系統現有設計]

**原始問題：**
- [問題A 及位置]
- [問題B 及位置]

---

### 決策理由
針對每個重要的修改，說明「為什麼選擇這個方案」而非其他替代方案：

**變更 1：[描述]**
- 選擇方案：[做法]
- 捨棄方案：[其他考慮過的做法及捨棄原因]

---

### 變更摘要
| 檔案 | 行號 | 變更類型 | 說明 |
|------|------|----------|------|
| `Foo.java` | 42 | Bug Fix | [描述] |
| `Bar.java` | 87–103 | Refactor | [描述] |

---

### 測試驗證
- [測試名稱]：✅ 通過
- [新增測試]：✅ 已建立，覆蓋 [場景]

---

### Reviewer 建議閱讀順序
1. 先閱讀 `Research 發現` 了解背景
2. 閱讀 `決策理由` 理解為什麼這樣改
3. 再看 PR diff

### 待討論事項（非本次範圍但建議討論）
- [若有發現但本次未處理的問題]
````

### 建議附在 PR 的方式

1. 將 `.ai-review/YYYY-MM-DD_pr-context_[描述].md` 的內容貼入 PR description
2. 或在 PR description 加上連結：`詳見 [AI Review Context](.ai-review/...)`
3. 讓 reviewer 在看 diff 前先閱讀此文件

---

## Java 特定審查重點

### 邏輯正確性
- Null 處理（NPE 風險）、`Optional` 的使用方式
- 例外處理是否恰當（checked vs unchecked，不要吃掉例外）
- 集合操作的邊界條件（空集合、單一元素）
- 多執行緒下的 race condition

### 效能
- N+1 查詢問題（JPA/Hibernate：`@OneToMany` 未加 `fetch = LAZY` 或未用 JOIN FETCH）
- 不必要的物件建立或 autoboxing（`Integer` vs `int`）
- Stream 操作效率（避免多次 `.filter().map()` 可合併）
- `synchronized` 範圍過大

### 安全性
- SQL injection（JDBC 原生查詢未用 PreparedStatement）
- 不安全的反序列化（`ObjectInputStream`）
- 敏感資訊洩漏（日誌中印出密碼、token、PII）
- 輸入驗證缺失（Controller 層未做 `@Valid`）

### 程式碼風格
- 方法超過 30 行通常是拆分信號
- 類別職責是否單一（SRP）
- 重複程式碼（DRY）
- 命名是否清晰表達意圖（避免 `data`、`info`、`temp`）
