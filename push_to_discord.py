#!/usr/bin/env python3
"""Push SocialRadar candidate posts to a Discord webhook as embeds.

Input: a JSON file matching no1_candidates_schema.md.
Webhook URL is read from the DISCORD_WEBHOOK_URL environment variable,
never from a CLI argument or hardcoded value.
"""
import json
import os
import ssl
import sys
import urllib.request

MAX_DESC_CHARS = 4000
BATCH_SIZE = 10

# Some Python installs (notably python.org builds on macOS) ship without a
# configured CA bundle, so the default SSL context can't verify any HTTPS
# host. Fall back to the OS trust store paths urllib's default misses.
_FALLBACK_CAFILES = ["/etc/ssl/cert.pem"]


def build_ssl_context():
    context = ssl.create_default_context()
    default_cafile = ssl.get_default_verify_paths().cafile
    if default_cafile and os.path.exists(default_cafile):
        return context
    for cafile in _FALLBACK_CAFILES:
        if os.path.exists(cafile):
            return ssl.create_default_context(cafile=cafile)
    return context


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


def send_batch(webhook_url, content, embeds, ssl_context):
    payload = {"embeds": embeds}
    if content:
        payload["content"] = content
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SocialRadar-ContentMonitor/1.0 (+https://github.com/almightyken0425/SocialRadar)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=ssl_context) as resp:
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

    ssl_context = build_ssl_context()

    for i in range(0, len(posts), BATCH_SIZE):
        batch = posts[i : i + BATCH_SIZE]
        embeds = [build_embed(p) for p in batch]
        content = header if i == 0 else ""
        status = send_batch(webhook_url, content, embeds, ssl_context)
        print(f"batch {i // BATCH_SIZE + 1}: {len(embeds)} embeds, status {status}")


if __name__ == "__main__":
    main()
