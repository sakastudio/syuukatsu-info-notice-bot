import os

import pymysql
import pymysql.cursors
import getreplies
import hashlib


def run():
    messages = getreplies.get_channel_to_message(channel=os.environ['SLACK_DATA_CHANNEL_ID'])
    new_message = []

    conn = pymysql.connect(host='host_name',
                           user='user_name',
                           db='db_name',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    # mySqlにそのメッセージのハッシュ値を問い合わせする
    select_sql = "SELECT msg_hs FROM msg_hs_list WHERE msg_hs = %s"
    insert_sql = "INSERT INTO msg_hs_list (msg_hs) VALUES (%s)"
    for msg in messages:
        msg_hs = hashlib.sha224(msg['text'].encode()).hexdigest()
        conn.cursor().execute(select_sql, (msg_hs,))
        result = conn.cursor().fetchall()

        # あったら次のメッセージへ
        if 0 < len(result): continue

        # なかったらDBにインサートし、新しいメッセージリスト
        conn.cursor().execute(insert_sql, msg_hs)
        new_message.append(msg)

    # TODO メッセージを送信する