# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
#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
import openai
import streamlit as st
import nbformat
import streamlit as st
import subprocess
import sys
from io import StringIO
import pandas as pd
from github import Github
import time
# import cv2 as cv
import glob
import io


with st.sidebar:
    st.title('🤖💬 SmatAnalysis Appz')
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    user = st.text_input('Enter Email:')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')


    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        g = Github('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')
        repo = g.get_repo('phaks323/My-analysis-bot')

        df = pd.read_csv(uploaded_file)
        df.to_csv(user + '.csv')
    
        ts = time.time()
        with open(user + '.csv', 'r') as file:
            data = file.read()

        repo.create_file(str(ts) + '.csv', 'upload csv', data, branch='master')


            

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = "" 
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        vv = full_response.partition(":")[2].split('print("# Done")')[0]
   
    st.markdown(vv)
with open('script.py','r') as f:

	newlines = []
	i = 0
	for line in f:
		if "plt.show()" in line:
			newlines.append(line.replace('plt.show()', "plt.savefig('"+ str(i) +".png') \nplt.close()"))
			i = i + 1
		else:
			newlines.append(line)
with open('script.py', 'w') as f:
                        for line in newlines:
                            f.write(line)
subprocess.run([f"{sys.executable}", "script.py"])


# for img in glob.glob("*.png"):
#     cv_img = cv.imread(img)
#     st.image(cv_img, caption='Sunrise by the mountains')


