import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import re
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
    return " ".join([entry['text'] for entry in transcript])

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-4でもOK（速度や料金次第）
        messages=[
            {"role": "system", "content": "以下のYouTube文字起こしを日本語で簡潔に要約してください。"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

st.title("YouTube要約ツール（スマホ対応）")

url = st.text_input("YouTubeのURLを入力してください")

if st.button("要約する") and url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            transcript = get_transcript(video_id)
            summary = summarize_text(transcript)
            st.subheader("要約結果")
            st.write(summary)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.error("正しいURLを入力してください")
