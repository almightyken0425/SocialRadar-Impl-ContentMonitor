# 候選貼文 JSON 輸入格式

`push_to_discord.py` 讀取單一 JSON 檔，結構如下。

- `content`：字串，選填，整批推播的開頭文字，只出現在第一批訊息
- `posts`：陣列，每筆代表一篇通過 Spec 判斷邏輯的候選貼文
  - `author`：字串，必填，貼文作者帳號
  - `content`：字串，必填，貼文原文，不經摘要或改寫
  - `url`：字串，必填，原文連結
  - `likes`：數字，選填，讚數
  - `comments`：數字，選填，留言數
  - `time_label`：字串，選填，發文時間的人讀標籤，例如 1小時前

範例：

```json
{
  "content": "SocialRadar 巡邏結果\n候選 1 篇",
  "posts": [
    {
      "author": "@example_user",
      "content": "貼文原文逐字放進來。",
      "url": "https://www.threads.net/@example_user/post/xxxxx",
      "likes": 12,
      "comments": 3,
      "time_label": "1小時前"
    }
  ]
}
```
