"""Question answering app in Streamlit.

Originally based on this template:
https://github.com/hwchase17/langchain-streamlit-template/blob/master/main.py

Run locally as follows:
> PYTHONPATH=. streamlit run chapter4/question_answering/app.py

Alternatively, you can deploy this on the Streamlit Community Cloud
or on Hugging Face Spaces. For Streamlit Community Cloud do this:
1. Create a GitHub repo
2. Go to Streamlit Community Cloud, click on "New app" and select the new repo
3. Click "Deploy!"
"""


import streamlit as st
import virus_total_tool
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

from agent import load_agent, openai_file_analysis
from utils import MEMORY

st.set_page_config(page_title="HaqAnalysis", page_icon=":robot:")
st.header("Upload a file and watch the results come in")

#LOGGER.info("Upload a file")
uploaded_files = st.file_uploader(
    label="Upload files",
    type=None,
    accept_multiple_files=False,
)

if not uploaded_files:
    st.info("Please upload a file to get started.")
    st.stop()

strategy = st.radio(
    "Reasoning strategy",
    (
        "plan-and-solve",
        "zero-shot-react",
    ),
)

tool_names = st.multiselect(
    "Which tools do you want to use?",
    [
        "Virus total API",
        "llm-math",
        "wikipedia",
        "google-search",
    ],
    ["Virus total API"],
)

if st.sidebar.button("Clear message history"):
    MEMORY.chat_memory.clear()

avatars = {"human": "user", "ai": "assistant"}
for msg in MEMORY.chat_memory.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

assert strategy is not None
agent_chain = load_agent(tool_names=tool_names, strategy=strategy)

if st.button("Run"):
    st.write("File uploaded successfully!")
    with st.spinner("Analysing the file"):
        file_attributes = virus_total_tool.getFileAttributes("test")
        st.write(f"File hash: {file_attributes}")

    with st.spinner("Analysing file attributes with OpenAI..."):
        analysis = openai_file_analysis(file_attributes)
        st.write("### Analysis:")
        st.write(analysis)