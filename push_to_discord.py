#!/usr/bin/env python3
"""Push SocialRadar candidate posts to a Discord webhook as embeds.

Input: a JSON file matching no1_candidates_schema.md.
Webhook URL is read from the DISCORD_WEBHOOK_URL environment variable,
never from a CLI argument or hardcoded value.
"""
import json
import os
import sys
import urllib.request

MAX_DESC_CHARS = 4000
BATCH_SIZE = 10


def build_embed(post):
    description = post["content"]
    if len(description) > MAX_DESC_CHARS:
        description = description[:MAX_DESC_CHARS] + "…"

    footer_parts = []
    if post.get("likes") is not None:
        footer_parts.append(f"讚 {post['likes']}")
    if post.get("comments") is not None:
        footer_parts.append(f"留言 {post['comments']}")
    if post.get("time_label"):
        footer_parts.append(post["time_label"])

    return {
        "title": post["author"],
        "description": description,
        "url": post["url"],
        "footer": {"text": "・".join(footer_parts)},
    }


def send_batch(webhook_url, content, embeds):
    payload = {"embeds": embeds}
    if content:
        payload["content"] = content
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    if len(sys.argv) != 2:
        print("Usage: push_to_discord.py <candidates.json>", file=sys.stderr)
        sys.exit(1)

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("錯誤：未設定 DISCORD_WEBHOOK_URL 環境變數", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    header = data.get("content", "")

    if not posts:
        print("候選清單為空，不送出任何請求")
        return

    for i in range(0, len(posts), BATCH_SIZE):
        batch = posts[i : i + BATCH_SIZE]
        embeds = [build_embed(p) for p in batch]
        content = header if i == 0 else ""
        status = send_batch(webhook_url, content, embeds)
        print(f"batch {i // BATCH_SIZE + 1}: {len(embeds)} embeds, status {status}")


if __name__ == "__main__":
    main()
