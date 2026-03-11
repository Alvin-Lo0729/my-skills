# My Claude Code Skills

個人 Claude Code Skills 集合，涵蓋文件處理、程式開發、創意設計、學習工具等多種類型。

---

## Skills 總覽

共 **29 個 Skills**，依類別分組如下：

---

### 文件處理

| Skill | 功能描述 |
|-------|---------|
| [docx](./docx/) | 建立、讀取、編輯和操作 Word 文件（.docx），支援追蹤修改、評論和格式化 |
| [pdf](./pdf/) | 讀取、提取、合併、分割、旋轉、加浮水印、建立、填表和加密 PDF 檔案 |
| [pptx](./pptx/) | 建立、編輯、讀取和操作 PowerPoint 簡報（.pptx）檔案 |
| [xlsx](./xlsx/) | 建立、讀取、編輯和操作試算表檔案（.xlsx、.csv、.tsv） |
| [markdown-to-epub](./markdown-to-epub/) | 將 Markdown 文件和聊天摘要轉換為格式化的 EPUB 電子書檔案 |

---

### 內容整理與翻譯

| Skill | 功能描述 |
|-------|---------|
| [content-summarizer](./content-summarizer/) | 將影片、網站或文字內容整理成結構化的繁體中文 Word 重點摘要檔案 |
| [translator](./translator/) | 將英文或日文翻譯成繁體中文，輸出雙語對照 Word 檔案（預設 .docx） |
| [youtube-transcript](./youtube-transcript/) | 使用 yt-dlp 從 YouTube 影片下載字幕，含 Whisper 轉錄備案 |
| [doc-coauthoring](./doc-coauthoring/) | 提供結構化的協作文件創作工作流：內容蒐集 → 精化 → 讀者測試 |
| [internal-comms](./internal-comms/) | 內部通訊資源和範本集合（狀態報告、專案更新、公司通訊等） |

---

### 程式開發

| Skill | 功能描述 |
|-------|---------|
| [claude-api](./claude-api/) | 使用 Claude API 或 Anthropic SDK 構建應用程式的指南和最佳實踐 |
| [java-review](./java-review/) | Java 專案完整程式碼審查工作流：Research → Plan → Implement，含 PR 脈絡同步 |
| [rpi-coder](./rpi-coder/) | Java 程式碼審查與重構，採用三階段工作流，強制人工確認後才進入實作 |
| [mcp-builder](./mcp-builder/) | 建立高品質 MCP（Model Context Protocol）伺服器的指南（Python / TypeScript） |
| [test-driven-development](./test-driven-development/) | 實踐 TDD：先寫失敗測試，再寫最少程式碼通過測試，適用所有功能開發 |
| [webapp-testing](./webapp-testing/) | 使用 Playwright 互動和測試本地網頁應用程式，支援截圖與日誌檢視 |
| [web-artifacts-builder](./web-artifacts-builder/) | 使用 React、Tailwind CSS 和 shadcn/ui 構建複雜的多元件 HTML 製品 |
| [skill-creator](./skill-creator/) | 創建新 Skill、修改現有 Skill、執行 Eval 測試與基準化效能 |

---

### 視覺設計與創意

| Skill | 功能描述 |
|-------|---------|
| [frontend-design](./frontend-design/) | 創建具有高設計品質的生產級前端介面，避免通用 AI 美學 |
| [canvas-design](./canvas-design/) | 創建視覺藝術（PDF 和 PNG），結合設計哲學：形式、空間、配色與構圖 |
| [algorithmic-art](./algorithmic-art/) | 使用 p5.js 創建具有隨機種子和互動參數探索的演算法藝術 |
| [imagen](./imagen/) | 使用 Google Gemini 的圖像生成能力建立圖片 |
| [image-enhancer](./image-enhancer/) | 提升圖像品質：提升解析度、增強銳度、縮減雜訊 |
| [slack-gif-creator](./slack-gif-creator/) | 建立 Slack 最適化的動態 GIF，含動畫概念、工具和最佳化策略 |
| [theme-factory](./theme-factory/) | 應用預設主題或建立自訂主題到任何製品（投影片、文件、HTML 等） |
| [brand-guidelines](./brand-guidelines/) | 應用 Anthropic 官方品牌配色、字體和視覺風格到任何製品 |

---

### 學習與效率

| Skill | 功能描述 |
|-------|---------|
| [anki-word-importer](./anki-word-importer/) | 自動從 Oxford 和 Cambridge 字典抓取音標與定義，製作可直接匯入 Anki 的單字卡 |
| [teaching-mode](./teaching-mode/) | 啟用教學模式，改變 Claude 的回答風格，適合學習導向對話 |
| [tailored-resume-generator](./tailored-resume-generator/) | 分析職位描述並生成客製化履歷，突顯相關經驗和技能以提高面試機會 |

---

## 快速查找

- 想整理 YouTube 影片重點 → [content-summarizer](./content-summarizer/)
- 想翻譯英文/日文 → [translator](./translator/)
- 想做 Java Code Review → [java-review](./java-review/)
- 想建立 MCP Server → [mcp-builder](./mcp-builder/)
- 想生成圖片 → [imagen](./imagen/)
- 想製作 Anki 單字卡 → [anki-word-importer](./anki-word-importer/)
- 想建立新 Skill → [skill-creator](./skill-creator/)


## 參考文件

MCP 与 Agent Skills：AI Agent 能力扩展的两块基石
https://zhuanlan.zhihu.com/p/2010662054764246320

MCP 伺服器 vs 工具 vs Agent 技能
https://blog.logto.io/zh-TW/mcp-tools-agentskill

Claude Code Skills：讓 AI 變身專業工匠
https://kaochenlong.com/claude-code-skills
