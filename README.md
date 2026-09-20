# GitHub Streak Reminder

매일 한국 시간 오전 9시(깃허브 잔디 타이머 초기화 시점)에, 직전 하루 동안
커밋을 했는지 확인해서 Pushbullet으로 핸드폰에 알림을 보내는 스크립트.

## 사용 방법

1. `.env.example`을 복사해서 `.env` 파일 생성
2. `.env` 파일에 본인 토큰 값 입력
3. 가상환경 활성화 후 `pip install -r requirements.txt`
4. `python3 github_reminder.py` 로 실행