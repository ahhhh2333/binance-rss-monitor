#!/usr/bin/env python3
"""
binance_rss_monitor.py
零 Token 监控 @binancezh 推文
关键词：alpha / 积分 / 活动（大小写不敏感）
已推送过的不再推送
"""
import os
import hashlib
import requests
import feedparser

RSS_URL     = "https://nitter.net/binancezh/rss"
WEBHOOK_URL = os.getenv("WECHAT_WEBHOOK_URL")
SEEN_FILE   = "seen.txt"

KEYWORDS = {"alpha", "积分", "活动"}

def load_seen() -> set:
    return set(open(SEEN_FILE).read().splitlines()) if os.path.exists(SEEN_FILE) else set()

def save_seen(s: set) -> None:
    open(SEEN_FILE, "w").write("\n".join(s))

def push_wechat(msg: str) -> None:
    requests.post(WEBHOOK_URL, json={"msgtype": "text", "text": {"content": msg}}, timeout=10)

def main() -> None:
    seen = load_seen()
    feed = feedparser.parse(RSS_URL)
    for entry in reversed(feed.entries):
        key = hashlib.md5(entry.link.encode()).hexdigest()
        if key in seen:
            continue
        title = entry.title.lower()
        if any(k in title for k in KEYWORDS):
            msg = f"【币安 Alpha 新推文】\n{entry.title}\n{entry.link}"
            push_wechat(msg)
            seen.add(key)
            print(f"📤 已推送：{entry.title[:50]}…")
    save_seen(seen)

if __name__ == "__main__":
    main()
