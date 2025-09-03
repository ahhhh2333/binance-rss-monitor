#!/usr/bin/env python3
import os, hashlib, requests, feedparser, datetime

RSS_URL     = "https://rsshub.app/twitter/user/binancezh"
WEBHOOK_URL = os.getenv("WECHAT_WEBHOOK_URL")
KEYWORDS    = {"alpha", "积分", "活动"}

feed = feedparser.parse(RSS_URL)
print("RSS 状态:", feed.status, len(feed.entries), "条")

for entry in feed.entries[:3]:            # 只看最近 3 条
    title = entry.title.lower()
    if any(k in title for k in KEYWORDS):
        msg = f"【推送】{entry.title}\n{entry.link}"
        requests.post(WEBHOOK_URL, json={"msgtype":"text","text":{"content":msg}}, timeout=10)
        print("已推送:", entry.title)
