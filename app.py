import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler

from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder



load_dotenv()

def create_agent_chain():
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        temperature=os.environ["OPENAI_API_TEMPERATURE"],
        #ストリーミング応答
        streaming=True,
        
    )
    
    # OpenAI Functions AgentのプロンプトにMemoryの会話履歴を追加するための設定
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        
    }
    # OpenAI Functions Agentが使える設定でMemoryを初期化
    memory = ConversationBufferMemory(memory_key="memory", return_Messages=True)
    
    #ツールの選択
    tools = load_tools(["ddg-search", "wikipedia"])
    return initialize_agent(
        tools, 
        chat, 
        agent = AgentType.OPENAI_FUNCTIONS,
        
        #以下追記
        agent_kwargs = agent_kwargs,
        memory = memory,
        ) #初期化


import streamlit as st
st.title("langchain-streamlit-app")

if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:#セッション内のメッセージ数だけでループ
    with st.chat_message(message["role"]):#ロールごとに
        st.markdown(message["content"])#保存されているテキストを表示

prompt = st.chat_input("What is up?")
#print(prompt)



if prompt:
    #ユーザー入力内容をst.session_state.messagesに追加
    st.session_state.messages.append({"role":"user", "content": prompt})
    
    with st.chat_message("user"):#ユーザーアイコン
        st.markdown(prompt)
        
        
        
    with st.chat_message("assistant"):#AIのアイコン
        #response = "こんにちは"
        #st.markdown(response)
        chat = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )
        messages = [HumanMessage(content=prompt)]
        response = chat(messages)
        st.markdown(response.content)
        
        
        
    with st.chat_message("assistant"):
        #ストリーミング応答の表示
        callback = StreamlitCallbackHandler(st.container())
        
        #agent_chain = create_agent_chain()
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        st.markdown(response)
        
        
        
        
    #応答をst.session_state.messagesに追加
    st.session_state.messages.append({"role": "assistant", "content": response})
    

    


