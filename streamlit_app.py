import streamlit as st
import openai
from PIL import Image

# ✅ 配置 OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

# ✅ 页面设置
st.set_page_config(page_title="Bohan Yue's AI Career Assistant")
st.title("🤖 Bohan Yue's AI Career Assistant")

# ✅ 加载头像（本地图片路径）
try:
    user_avatar = Image.open("images/bohan_avatar.png")
except:
    user_avatar = None

try:
    assistant_avatar = Image.open("images/assistant_avatar.png")
except:
    assistant_avatar = None

# ✅ 初始化 thread 和聊天记录
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.session_state.messages = []

# ✅ 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=user_avatar if message["role"] == "user" else assistant_avatar):
        st.markdown(message["content"])

# ✅ Assistant 开场欢迎语（只显示一次）
if not st.session_state.messages:
    assistant_intro = "👋 Hi there! I’m Bohan’s AI career assistant. Feel free to ask me about his experience, skills, and fit for your role."
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown(assistant_intro)
    st.session_state.messages.append({"role": "assistant", "content": assistant_intro})

# ✅ 聊天输入框
user_input = st.chat_input("Ask anything about Bohan...")

if user_input:
    # 显示用户输入 + 存入历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_input)

    # 发消息到 Assistant
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # 创建 Assistant 回应
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

        # 显示 Assistant 回复 + 存入历史
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant", avatar=assistant_avatar):
            st.markdown(assistant_reply)

