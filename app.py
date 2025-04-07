import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube文字起こしコピーツール", layout="centered")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
    return " ".join([entry['text'] for entry in transcript])

st.title("📋 YouTube文字起こしコピーツール")
st.write("YouTubeのURLを入力すると、文字起こしが表示されます。最初に『要約して』が付きます。")

url = st.text_input("🔗 YouTubeのURLを入力してください")

if st.button("文字起こしを取得する") and url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            transcript = get_transcript(video_id)
            final_text = "要約して\n\n以下の文章を要約して：\n\n" + transcript
            st.success("以下の文字をそのままコピーして、ChatGPTに貼ってください👇")
            st.code(final_text, language='text')

            # 自動で選択されるようにする（JSスクリプト）
            st.markdown(
                """
                <script>
                const textarea = window.parent.document.querySelector('textarea');
                if (textarea) {
                    textarea.focus();
                    textarea.select();
                }
                </script>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"文字起こしの取得中にエラーが発生しました：{e}")
    else:
        st.error("正しいYouTubeのURLを入力してください")
