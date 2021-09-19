import json
import os
from slack_sdk import WebClient


# メッセージからリプライを取得
def get_message_to_reply(channel, ts):
    # APIを叩く
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = client.conversations_replies(channel=channel, ts=ts)

    # メッセージをすべて返す
    messages = []
    for msg in response['messages']:
        messages.append(msg)
    return messages


# チャンネルからリプライを含むメッセージを取得
def get_channel_to_message(channel):
    # APIを叩く
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = client.conversations_history(channel=channel)
    messages = []

    # レスポンスをチェック
    for msg in response['messages']:
        # メッセージでなければ次へ
        if msg['type'] != 'message':
            continue

        # リプライがついて無ければそのまま登録
        if not ('reply_count' in msg.keys()):
            messages.append(msg)
            continue

        # リプライがついていればリプライを取得する
        if 1 < msg['reply_count']:
            messages = messages + get_message_to_reply(channel, msg['ts'])
        else:
            messages.append(msg)
    return messages
