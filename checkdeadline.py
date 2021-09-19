# "応募締め切り"があるか調べ、あったら日付がたを返す
import datetime
import re


def check(string):
    # 1行ごとに応募締切に関する文言が内科チェックする
    for line in string.split('\n'):
        # 締切に関する言葉が含まれてなかったら次へ
        if "応募締切" not in line and \
                "応募締め切り" not in line and \
                "締め切り" not in line and \
                "締切" not in line: continue
        try:
            # 正規表現で日付のみを抽出
            date_str = re.search(r"20[0-9]{2}/(0[1-9]|1[0-2]|[1-9])/(0[1-9]|[12][0-9]|3[01]|[1-9])", line)
            date = datetime.datetime.strptime(date_str.group(), "%Y/%m/%d")
            return True, date
        except:
            # なかったかエラーをスローしたら1970年で返す
            return False, datetime.date(year=1970, month=1, day=1)
    return False, datetime.date(year=1970, month=1, day=1)
