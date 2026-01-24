import streamlit as st
import yt_dlp

st.set_page_config(page_title="My YouTube Streamer", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Direct Streamer")
st.caption("No Ads, No Downloads, Just Watch.")

# Input for URL
url = st.text_input("YouTube URL을 입력하세요", placeholder="https://youtu.be/...")

if url:
    try:
        with st.spinner("비디오 주소를 추출하는 중..."):
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # Prefer MP4 for best compatibility
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_url = info_dict.get('url', None)
                video_title = info_dict.get('title', 'Unknown Title')
                
                if video_url:
                    st.success(f"재생 준비 완료: {video_title}")
                    st.video(video_url)
                else:
                    st.error("비디오 주소를 찾을 수 없습니다.")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.markdown("---")
st.info("💡 팁: 아이폰 Safari에서 '홈 화면에 추가'를 하면 앱처럼 쓸 수 있습니다.")
