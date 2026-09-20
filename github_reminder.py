import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

PUSHBULLET_TOKEN = os.environ.get("PUSHBULLET_TOKEN")
GITHUB_USERNAME =  os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# print(GITHUB_USERNAME)

PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"

def send_pushbullet_notification(title: str, body: str) -> None:
    response = requests.post(
        PUSHBULLET_URL,
        headers = {"Access-Token": PUSHBULLET_TOKEN},
        json = {"type": "note", "title": title, "body": body},
        timeout = 10,
    )
    response.raise_for_status()


GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_yesterday_utc_contribution_count() -> int:
    now_utc = datetime.now(timezone.utc)
    yesterday = (now_utc - timedelta(days=1)).date()

    from_time = f"{yesterday.isoformat()}T00:00:00Z"
    to_time = f"{yesterday.isoformat()}T23:59:59Z"

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    variables = {"login": GITHUB_USERNAME, "from": from_time, "to": to_time}

    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json = {"query": query, "variables": variables},
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout = 10,
    )
    response.raise_for_status()
    data = response.json()

    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

def main():
    try:
        count = get_yesterday_utc_contribution_count()
    except Exception as e:
        send_pushbullet_notification(
            "깃허브 리마인더 오류",
            f"스트릭 확인 중 오류 발생: {e}",
        )
        return

    if count > 0:
        title = "🔥 깃허브 잔디 타이머 초기화"
        body = f"어제 커밋 {count}개! 오늘도 이어가요."
    else:
        title = "⚠️ 깃허브 잔디 타이머 초기화"
        body = "어제 커밋 기록이 없어요. 스트릭이 끊겼을 수 있어요 — 오늘 다시 시작해요!"

    send_pushbullet_notification(title, body)

if __name__ == "__main__":
    main()

# get_yesterday_utc_contribution_count()
# send_pushbullet_notification("Test", "check it out")