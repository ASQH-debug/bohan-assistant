# app.py
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

st.set_page_config(page_title="Bohan's Career Assistant")
st.title("🤖 Bohan Yue's AI Career Assistant")

# 初始化对话线程
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

# 聊天输入框
user_input = st.chat_input("Ask anything about Bohan's background, experience, or fit...")

if user_input:
    st.chat_message("user").write(user_input)

    # 添加问题
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # Assistant 开始回应
    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    with st.spinner("Thinking..."):
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        messages = openai.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )
        assistant_reply = messages.data[0].content[0].text.value
        st.chat_message("assistant").write(assistant_reply)
