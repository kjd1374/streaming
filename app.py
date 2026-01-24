import streamlit as st
import yt_dlp
import json
import os

# --- Configuration ---
st.set_page_config(page_title="My YouTube Streamer", page_icon="🎬", layout="wide")
CHANNELS_FILE = "channels.json"

# --- Functions ---
def load_channels():
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_channels(channels):
    # Note: Streamlit Cloud resets files on reboot, but this works for session/local persistence
    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, ensure_ascii=False, indent=4)

@st.cache_data(ttl=3600)  # Cache results for 1 hour to speed up
def get_channel_videos(channel_url):
    ydl_opts = {
        'extract_flat': True,  # Don't download, just get metadata
        'playlistend': 10,     # Get latest 10 videos
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                return info['entries']
        except Exception as e:
            st.error(f"Error fetching channel: {e}")
            return []
    return []

def get_stream_url(video_url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get('url'), info.get('title')

# --- Sidebar: Channel Management ---
st.sidebar.title("📺 채널 목록")

channels = load_channels()
channel_names = [c['name'] for c in channels]

# Selection
selected_channel_name = st.sidebar.radio("채널 선택", ["직접 입력"] + channel_names)

# Add New Channel
with st.sidebar.expander("➕ 채널 추가/삭제"):
    new_name = st.text_input("이름")
    new_url = st.text_input("URL (채널 메인 주소)")
    if st.button("추가"):
        if new_name and new_url:
            channels.append({"name": new_name, "url": new_url})
            save_channels(channels)
            st.rerun()
            
    # Remove Channel (Simple version: remove selected)
    if selected_channel_name != "직접 입력":
        if st.button(f"'{selected_channel_name}' 삭제"):
            channels = [c for c in channels if c['name'] != selected_channel_name]
            save_channels(channels)
            st.rerun()

# --- Main Content ---
st.title("🎬 YouTube Direct Streamer")

video_url_to_play = None

if selected_channel_name == "직접 입력":
    st.info("보고 싶은 영상의 주소를 직접 입력하세요.")
    video_url_to_play = st.text_input("YouTube URL", placeholder="https://youtu.be/...")
else:
    # Find selected channel URL
    selected_channel = next((c for c in channels if c['name'] == selected_channel_name), None)
    if selected_channel:
        st.header(f"📺 {selected_channel_name}")
        
        with st.spinner(f"'{selected_channel_name}'의 최신 영상을 가져오는 중..."):
            videos = get_channel_videos(selected_channel['url'])
            
        if videos:
            # Display videos in a grid
            cols = st.columns(2)  # Mobile friendly 2 columns
            for idx, video in enumerate(videos):
                with cols[idx % 2]:
                    # Create a container with border for each video card
                    with st.container(border=True):
                        # Construct watch URL
                        v_url = f"https://www.youtube.com/watch?v={video['id']}"
                        
                        # Display Thumbnail (if available) - yt-dlp flat extraction might limit high-res thumbnails, but usually returns 'thumbnails'
                        # For flat playlist, thumbnails might not be fully populated or just a list. Safe fallback.
                        # video['title'] is main.
                        
                        st.markdown(f"**{video.get('title', 'No Title')}**")
                        
                        if st.button("재생 ▶", key=video['id']):
                            video_url_to_play = v_url
                            
        else:
            st.warning("영상을 찾을 수 없습니다.")

# --- Video Player ---
if video_url_to_play:
    st.markdown("---")
    with st.spinner("재생 준비 중..."):
        try:
            stream_url, title = get_stream_url(video_url_to_play)
            if stream_url:
                st.success(f"재생 중: {title}")
                st.video(stream_url)
            else:
                st.error("재생할 수 없는 영상입니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.markdown("---")
st.caption("Tip: 왼쪽 사이드바에서 채널을 추가하면 리스트에 유지됩니다. (브라우저 캐시 삭제 시 초기화 될 수 있음)")
