import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key="GOOGLE_API_KEY")
prompt="""You are video summarizer. You will be taking the transcript text and summarize the entire video and you will be providing the summary points which are important in 300 words. Please provide the summary given here:"""
def extratct_transcript(url):
  try:
    video_id=url.split("=")[1]
    transcript=YouTubeTranscriptApi.get_transcript(video_id)

    transcript_text=""
    for i in transcript:
      transcript_text += " "+i["text"]
    return transcript_text
    pass
  except Exception as e:
    raise e
def gemini_content(transcript_text,prompt):
  model=genai.GenerativeModel("gemini-pro")
  response=model.generate_content(prompt+transcript_text)
  return response.text
st.title("Video Summarize")
video_url=st.text_input("Enter the Video URL: ")
if video_url:
    video_id = video_url.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Summarize"):
        transcript_text = extratct_transcript(video_url)

        if transcript_text:
            summary = gemini_content(transcript_text, prompt)
            st.write(summary)
