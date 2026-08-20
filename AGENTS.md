# SocialRadar Content Monitor Impl 規則

- 本 repo 是 Module Impl git
- 產品為 SocialRadar
- module id 為 `no1_content_monitor`

## 多層配對

- Spec git 是本 module 的行為規格仲裁端，位於同產品 `no3_product_specs/no1_content_monitor/`
- Design git 不建立，profile 為 app_basic
- 配對以 `decision_framework_router` 的註冊表為準

---

## 架構分工

- 抓取與篩選判斷段落由 Claude in Chrome 操作瀏覽器搭配 LLM 代理執行，不在本 repo 腳本化
- 組訊息與推播段落為機械式流程，由本 repo 的 `push_to_discord.py` 承載
- 抓取端輸出的候選貼文清單，格式須符合本 repo `no1_candidates_schema.md` 定義後，才能餵給推播腳本

---

## 目錄責任

- `push_to_discord.py`
  - 讀取候選貼文 JSON，組裝 Discord embed 並推播
  - Webhook 位址一律讀環境變數 `DISCORD_WEBHOOK_URL`，不寫死於程式碼
- `no1_candidates_schema.md`
  - 候選貼文 JSON 的輸入格式說明

---

## 原生工作規則

- 任何改動先使用 `decision_framework_router`
- Markdown 改動使用 `universal_writing_linter`
- Impl 變動要對照 Spec 的 `no3_logics/no1_content_monitor_logic.md`
- 跨層 branch 名稱必須一致
- 配對 commit 內容必須一致
- Webhook URL、API Key 等密鑰不得寫入本 repo 任何檔案

---

## 相容與漂移控制

- `AGENTS.md` 是本目錄的規則真相
- `CLAUDE.md` 只保留 Claude Code 入口
- 產品規則不得複製回相容入口
- 漂移檢查確認相容入口只含導向規則
