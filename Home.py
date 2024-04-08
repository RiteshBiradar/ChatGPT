from openai import OpenAI;
import streamlit as st;
import os;


st.set_page_config(
    page_title="ChatGPT - Clone",
    page_icon="🤖"
)
st.header("ChatGPT - Clone ")

st.divider()
st.caption("Chat GPT can make mistakes. Consider checking important information.")


client = OpenAI(api_key=st.secrets["TOGETHER_API_KEY"], base_url=os.environ.get("TOGETHER_BASE_URL"))
st.session_state["openai_model"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"  #secure connection and fetch kare openai ki api se and communication build hori st and key mai

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"   #aggar gpt 3.5 nahi hai session_state mai tho usko assign kardera


if "messages" not in st.session_state:
    st.session_state.messages = []    #messages ki chat jo rahi thi usko ek empty array se assign kare

for messages in st.session_state.messages:
    with st.chat_message(messages["role"]): #with bole tho when I am doing something do these 
        st.markdown(messages["content"])  #jo message ka daba hai usko ek role and jo content aaya wo batara

if inputValue := st.chat_input("Message ChatGPT..."):
    st.session_state.messages.append({"role":"user","content" : inputValue})

    with(st.chat_message("user")):  #displays whatever the user has written on to the screen
        st.markdown(inputValue)  

    with st.chat_message("assistant"):
        message_placeholder = st.empty();  #wo jo logo raheta bot kaan wo develop hota ye 3 lines of code se
        full_response=""
    
    for response in client.chat.completions.create(
        model= st.session_state["openai_model"], #specifies which model to use 
        messages=[{"role" : m["role"], "content" : m["content"]} for m in st.session_state.messages], #It formats the messages stored in the st.session_state.messages list into the required format for the API call.
        stream=True # stream True matlab , puri api ek sath nahi aati ,  jiti mili uthna display hota raheta , it changes how the API responds to your request. Instead of waiting for the API to process everything and return a single response, setting stream=True tells the API to start sending partial responses as they become available, without waiting for the entire response to be ready.
    ):
        full_response += (response.choices[0].delta.content or "") #uska text ajata and delta used to represent new data is generated
        message_placeholder.markdown(full_response + "▌")  #wo bar(unicode) visual ka liya use hota ,  used to indicate the text is still going on
        
    message_placeholder.markdown(full_response) #final response when finished

    st.session_state.messages.append({"role": "assistant", "content": full_response}) #screen pe display karta
