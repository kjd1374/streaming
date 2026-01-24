# ☁️ Streamlit Cloud 배포 가이드

이제 만든 프로그램을 무료 서버(Streamlit Cloud)에 올려서 아이폰에서 접속해봅시다.

## 1단계: GitHub에 코드 올리기
1. [GitHub](https://github.com/new)에 로그인하여 **New Repository**를 만듭니다 (이름 예: `youtube-streamer`, **Public**으로 설정).
2. 아래 명령어를 터미널에 입력하여 코드를 올립니다. (GitHub에서 주어지는 주소 사용)
   ```bash
   git remote add origin https://github.com/YOUR_ID/youtube-streamer.git
   git branch -M main
   git push -u origin main
   ```

## 2단계: Streamlit Cloud 연결
1. [Streamlit Cloud](https://share.streamlit.io/)에 접속하여 로그인합니다 (GitHub 아이디로 로그인).
2. 오른쪽 위 **"New app"** 버튼을 누릅니다.
3. **"Use existing repo"**를 선택하고, 방금 만든 `youtube-streamer` 저장소를 선택합니다.
4. **"Deploy!"** 버튼을 누릅니다.

## 3단계: 아이폰에서 접속
1. 배포가 완료되면 화면 위에 **웹사이트 주소(URL)**가 나옵니다.
2. 이 주소를 복사해서 아이폰 Safari에 붙여넣으세요.
3. Safari 하단 공유 버튼(네모에 화살표) → **"홈 화면에 추가"**를 누르세요.
4. 이제 홈 화면에 생긴 아이콘을 누르면 앱처럼 실행됩니다! 🎉
