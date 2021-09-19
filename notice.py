import datetime
import os
import getreplies
import checkdeadline
import get_mention
from slack_sdk import WebClient


def run():
    # 返信を含むメッセージを取得
    messages = getreplies.get_channel_to_message(channel=os.environ['SLACK_DATA_CHANNEL_ID'])

    # 各日付メッセージ
    today = []
    one_day_ago = []
    three_day_ago = []
    seven_day_ago = []

    # 個人メンション用配列
    person_mention = []

    for msg in messages:
        # メッセージに含まれる日付を取得
        exist, date = checkdeadline.check(msg['text'])
        if not exist:
            continue
        # 日付の差を計算
        day_sub = (date.date() - datetime.date.today()).days

        # 各日付に応じて配列に格納
        if day_sub == 0:
            today.append(msg['text'])
            person_mention += get_mention.mention_user_list(msg)
        elif day_sub == 1:
            one_day_ago.append(msg['text'])
            person_mention += get_mention.mention_user_list(msg)
        elif day_sub == 3:
            three_day_ago.append(msg['text'])
            person_mention += get_mention.mention_user_list(msg)
        elif day_sub == 7:
            seven_day_ago.append(msg['text'])
            person_mention += get_mention.mention_user_list(msg)

    # 送信するテキストを組み立て

    # チャンネルにメンション
    # もし送信するものがなければメンションしない
    send_msg = ""
    if 0 >= len(today) and 0 >= len(one_day_ago) and 0 >= len(three_day_ago) and 0 >= len(seven_day_ago):
        send_msg = "本日通知の予定はありません"
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        response = client.chat_postMessage(channel=os.environ['SEND_CHANNEL_ID'], text=send_msg)
        exit()
    else:
        send_msg = "<!channel>\n"

    # 個人メンション
    person_mention = list(set(person_mention))
    for user in person_mention:
        send_msg += "<@{0}>".format(user)

    send_msg += "\n\n==================================================\n【締切1週間前】\n"
    # 7日前
    for msg in seven_day_ago:
        send_msg += "\n"
        send_msg += msg
        send_msg += "\n"

    send_msg += "\n\n\n\n\n\n\n==================================================\n【締切3日前】\n"
    # 7日前
    for msg in three_day_ago:
        send_msg += "\n"
        send_msg += msg
        send_msg += "\n"

    send_msg += "\n\n\n\n\n\n\n==================================================\n*【締切1日前】*\n"
    # 7日前
    for msg in one_day_ago:
        send_msg += "\n"
        send_msg += msg
        send_msg += "\n"

    send_msg += "\n\n\n\n\n\n\n==================================================\n*【本日締切】*\n"
    # 7日前
    for msg in today:
        send_msg += "\n"
        send_msg += msg
        send_msg += "\n"

    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    response = client.chat_postMessage(channel=os.environ['SEND_CHANNEL_ID'], text=send_msg)
