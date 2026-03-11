#!/usr/bin/env python3
"""
Anki Word Importer v3
- 自動抓取所有詞性，每個單字產生一個檔案
- 檔名格式：word.txt（所有意思合併，每行一個意思）
- 7 欄位：單字、音標+發音、詞性、英文解釋、中文解釋、範例、等級標籤

用法: python3 fetch_word.py <word>
"""

import sys
import os
import re
import time
import urllib.request

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

OUTPUT_DIR = os.path.expanduser("~/anki-import-file")
ANKI_MEDIA_DIR = os.path.expanduser(
    "~/Library/Application Support/Anki2/使用者 1/collection.media"
)

# ── HTML 工具 ─────────────────────────────────────────────────────────────────

def fetch_html(url, return_final_url=False):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            final_url = resp.url
            if return_final_url:
                return html, final_url
            return html
    except Exception as e:
        print(f"  [警告] 無法取得 {url}: {e}", file=sys.stderr)
        if return_final_url:
            return "", url
        return ""


def strip_tags(html_text):
    return re.sub(r"<[^>]+>", "", html_text).strip()


def find_class_blocks(html, tag, class_name):
    """找出所有符合 class 的 tag 區塊，正確處理巢狀"""
    pattern = re.compile(
        r'<' + tag + r'[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*>',
        re.IGNORECASE
    )
    results = []
    for m in pattern.finditer(html):
        start = m.start()
        depth = 0
        i = start
        while i < len(html):
            if html[i] == '<':
                if re.match(r'</' + tag + r'\s*>', html[i:], re.IGNORECASE):
                    depth -= 1
                    if depth == 0:
                        end = i + re.match(r'</' + tag + r'\s*>', html[i:], re.IGNORECASE).end()
                        results.append(html[start:end])
                        break
                elif re.match(r'<' + tag + r'[\s>]', html[i:], re.IGNORECASE):
                    depth += 1
            i += 1
    return results


def first_class_text(html, tag, class_name):
    blocks = find_class_blocks(html, tag, class_name)
    return strip_tags(blocks[0]) if blocks else ""


# ── Oxford：音標 + 音檔 ──────────────────────────────────────────────────────

def get_oxford_data(word):
    """回傳 (phonetic, audio_url, audio_filename)"""
    w = word.lower()
    first = w[0]
    audio_url = (
        f"https://www.oxfordlearnersdictionaries.com/media/english/"
        f"uk_pron/{first}/{w}/{w}__/{w}__gb_1.mp3"
    )

    phonetic = ""
    for suffix in ["", "_1", "_2"]:
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{w}{suffix}"
        html = fetch_html(url)
        if not html:
            continue
        for cls in ["phon", "phonetics"]:
            text = first_class_text(html, "span", cls)
            if text and "/" in text:
                phonetic = text.strip()
                break
        if not phonetic:
            m = re.search(r'class="[^"]*phon[^"]*"[^>]*>([^<]+)<', html)
            if m:
                phonetic = m.group(1).strip()
        if phonetic:
            parts = re.findall(r'/[^/]+/', phonetic)
            if parts:
                phonetic = parts[0]
            break
        time.sleep(0.5)

    return phonetic, audio_url


def download_audio(audio_url, word):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{word.lower()}__gb_1.mp3"
    out_path = os.path.join(OUTPUT_DIR, filename)
    try:
        req = urllib.request.Request(audio_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"  [音檔] 已下載 → {out_path}")

        # 同步複製到 Anki 媒體資料夾
        if os.path.isdir(ANKI_MEDIA_DIR):
            import shutil
            anki_dest = os.path.join(ANKI_MEDIA_DIR, filename)
            shutil.copy2(out_path, anki_dest)
            print(f"  [音檔] 已複製到 Anki 媒體資料夾 → {anki_dest}")
        else:
            print(f"  [警告] 找不到 Anki 媒體資料夾：{ANKI_MEDIA_DIR}", file=sys.stderr)

        return filename
    except Exception as e:
        print(f"  [警告] 音檔下載失敗: {e}", file=sys.stderr)
        return None


# ── Cambridge：所有詞性的所有意思 ──────────────────────────────────────────────

CEFR_LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}


def extract_cefr_level(block_html):
    """從 def-block HTML 中提取 CEFR 等級（如 B1、A2）"""
    # 嘗試多種 Cambridge 可能的 class 名稱
    for cls in ["epp-xref", "dlab-t", "guideword", "dlab"]:
        matches = re.findall(
            r'class="[^"]*' + cls + r'[^"]*"[^>]*>([^<]+)<', block_html
        )
        for m in matches:
            text = m.strip().upper()
            if text in CEFR_LEVELS:
                return text

    # fallback：直接在 block 開頭找 A1/B2 等字樣
    m = re.search(r'\b([ABC][12])\b', block_html[:500])
    if m and m.group(1) in CEFR_LEVELS:
        return m.group(1)
    return ""


def get_cambridge_data(word):
    """
    抓取 Cambridge 所有詞性的所有意思，並回傳 Cambridge 重新導向後的標準字形
    （例如：activities → activity）
    回傳 (canonical_word, list of dict):
      canonical_word: Cambridge 實際呈現的字頭（base form）
      list: { pos, english, chinese, example, level }
    """
    url = f"https://dictionary.cambridge.org/dictionary/english-chinese-traditional/{word.lower()}"
    html, final_url = fetch_html(url, return_final_url=True)
    if not html:
        return word.lower(), []

    # 從最終 URL 提取 Cambridge 標準字形（跟隨重新導向）
    canonical_word = word.lower()
    url_match = re.search(r'/dictionary/english-chinese-traditional/([^/?#]+)', final_url)
    if url_match:
        canonical_word = url_match.group(1).lower()

    meanings = []

    # 每個 entry-body__el = 一個詞性的完整詞條
    entry_blocks = find_class_blocks(html, "div", "entry-body__el")
    if not entry_blocks:
        entry_blocks = [html]

    for entry_html in entry_blocks:
        # 取得詞性標籤
        pos = ""
        pos_m = re.search(r'class="[^"]*\bpos\b[^"]*"[^>]*>([^<]+)<', entry_html)
        if pos_m:
            pos = pos_m.group(1).strip()

        # 找出所有個別定義 block
        def_blocks = find_class_blocks(entry_html, "div", "def-block")
        if not def_blocks:
            def_blocks = find_class_blocks(entry_html, "div", "ddef_block")

        for def_html in def_blocks:
            meaning = {"pos": pos}

            # CEFR 等級（A1/B1/C2...）
            meaning["level"] = extract_cefr_level(def_html)

            # 英文定義
            eng = ""
            for cls in ["ddef_d", "def ddef_d"]:
                eng = first_class_text(def_html, "div", cls)
                if not eng:
                    eng = first_class_text(def_html, "span", cls)
                if eng:
                    eng = re.sub(r":\s*$", "", eng).strip()
                    break
            meaning["english"] = eng

            # 中文翻譯
            chinese = ""
            for cls in ["trans dtrans", "dtrans", "trans"]:
                blocks = find_class_blocks(def_html, "span", cls)
                if blocks:
                    chinese = strip_tags(blocks[0]).strip()
                    if chinese:
                        break
            meaning["chinese"] = chinese

            # 英文範例
            example = ""
            for cls in ["eg deg", "deg", "eg"]:
                example = first_class_text(def_html, "span", cls)
                if example:
                    break
            meaning["example"] = example.strip()

            if meaning["english"]:
                meanings.append(meaning)

    return canonical_word, meanings


# ── 產生個別 Anki TSV 檔案 ───────────────────────────────────────────────────

TSV_HEADER = "\n".join([
    "#separator:tab",
    "#html:true",
    "#tags column:7",
    "#notetype:英文單字",
    "#deck:英文單字",
])

# Anki note type 欄位順序：
# 1:單字  2:音標  3:詞性  4:英文解釋  5:中文解釋  6:範例  7:標籤(tags)


def clean(text):
    """移除 tab 與換行，避免破壞 TSV 格式"""
    return re.sub(r"[\t\n\r]", " ", text).strip()


def write_word_file(word, phonetic_field, meanings):
    """將單字所有意思合併寫入一個 TSV 檔案，每行一個意思"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{word.lower()}.txt"
    out_path = os.path.join(OUTPUT_DIR, filename)

    rows = []
    for m in meanings:
        tag_parts = []
        if m["level"]:
            tag_parts.append(m["level"])
        if m["pos"]:
            tag_parts.append(m["pos"].replace(" ", "_"))

        row = "\t".join([
            clean(word),
            clean(phonetic_field),
            clean(m["pos"]),
            clean(m["english"]),
            clean(m["chinese"]),
            clean(m["example"]),
            clean(" ".join(tag_parts)),
        ])
        rows.append(row)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TSV_HEADER + "\n")
        f.write("\n".join(rows) + "\n")

    return out_path


# ── 主程式 ───────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python3 fetch_word.py <word>")
        sys.exit(1)

    word = sys.argv[1].strip()
    print(f"\n=== 處理單字: {word} ===")

    # 1. Cambridge 所有意思（同時取得標準字形）
    print("\n[1/3] 抓取 Cambridge 所有意思（所有詞性）...")
    canonical_word, meanings = get_cambridge_data(word)
    if canonical_word != word.lower():
        print(f"  Cambridge 重新導向：{word} → {canonical_word}（將使用標準字形查 Oxford）")
    print(f"  共取得 {len(meanings)} 個意思")

    if not meanings:
        print("  [警告] 未取得任何意思，請確認單字拼寫是否正確")
        sys.exit(1)

    # 依詞性統計
    pos_counts = {}
    for m in meanings:
        pos_counts[m["pos"]] = pos_counts.get(m["pos"], 0) + 1
    for p, c in pos_counts.items():
        print(f"    {p or '(未知詞性)'}: {c} 個意思")

    # 2. Oxford 音標 + 下載音檔（使用 Cambridge 取得的標準字形）
    print(f"\n[2/3] 抓取 Oxford 音標與音檔（查詢：{canonical_word}）...")
    time.sleep(1)
    phonetic, audio_url = get_oxford_data(canonical_word)
    print(f"  音標: {phonetic or '(未取得)'}")
    print(f"  音檔 URL: {audio_url}")

    audio_filename = download_audio(audio_url, canonical_word)

    # 音標欄位 = 音標文字 + [sound:檔名]（不含 URL）
    phonetic_field_parts = []
    if phonetic:
        phonetic_field_parts.append(phonetic)
    if audio_filename:
        phonetic_field_parts.append(f"[sound:{audio_filename}]")
    phonetic_field = "  ".join(phonetic_field_parts)

    # 3. 所有意思合併寫入單一檔案
    print("\n[3/3] 產生 Anki 匯入檔案...")
    for i, m in enumerate(meanings, 1):
        level_str = f" [{m['level']}]" if m["level"] else ""
        print(f"  {i:3}. [{m['pos']:12}]{level_str} {m['english'][:50]}...")

    out_path = write_word_file(
        word=canonical_word,
        phonetic_field=phonetic_field,
        meanings=meanings,
    )

    print(f"\n✅ 完成！{len(meanings)} 個意思合併為 1 個檔案")
    print(f"   位置：{out_path}")
    if audio_filename:
        print(f"   音檔：{audio_filename}")

    print()
    print("📌 Anki 匯入步驟：")
    print("   1. 在 Anki 建立名為「英文單字」的 Note Type，包含 6 個欄位：")
    print("      單字 / 音標 / 詞性 / 英文解釋 / 中文解釋 / 範例")
    print(f"   2. 選擇要匯入的檔案：檔案 → 匯入 → 選 {canonical_word}.txt")
    print("   3. 確認欄位對應順序正確（檔案內每行 = 一張卡片）")
    if audio_filename:
        print(f"   4. 將 {audio_filename} 複製到 Anki 媒體資料夾")
        print("      （工具 → 檢查媒體 可查看路徑）")


if __name__ == "__main__":
    main()
