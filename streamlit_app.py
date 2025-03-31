import streamlit as st
import openai
from PIL import Image

# 安全读取 API Key & Assistant ID
openai.api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

# ✅ 页面设置
st.set_page_config(page_title="Bohan's Career Assistant")
st.title("🤖 Bohan Yue's AI Career Assistant")

# ✅ 可选自定义头像（确保文件存在）
try:
    user_avatar = Image.open("images/bohan_avatar.png")
    assistant_avatar = Image.open("images/assistant_avatar.png")
except:
    user_avatar = None
    assistant_avatar = None

# ✅ 初始化 Thread 和历史消息
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.session_state.messages = []

# ✅ 首次加载欢迎语
if "welcome_shown" not in st.session_state:
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown("👋 Hi there! I’m Bohan’s AI career assistant. Feel free to ask me about his experience, skills, and fit for your role.")
    st.session_state.welcome_shown = True

# ✅ 聊天输入框
user_input = st.chat_input("Ask me anything about Bohan...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 显示用户消息
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_input)

    # 给 OpenAI 发送消息
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # 运行 Assistant
    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # 等待回应完成
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
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant", avatar=assistant_avatar):
            st.markdown(assistant_reply)

# ✅ 展示历史聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=user_avatar if message["role"] == "user" else assistant_avatar):
        st.markdown(message["content"])
