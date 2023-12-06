import streamlit as st
import openai
import pandas as pd
import json

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)

def translate():
    # Use ChatGPT API to translate Japanese to English
    prompt = 'Act as if you are a Japanese tutor. I will provide you a passage written in Japanese. Your task is to translate the passage into English.'
    all_messages = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=all_messages
    )
    translation = response.choices[0].message.content
    st.write(translation)

def get_vocabs():
    prompt = """Act as if you are a Japanese tutor. I will provide you a passage written in Japanese. 
            Your task is to choose 10 Japanese words suitable for beginners and list in a JSON array, one word per line. 
            Each word should should have 6 fields:
              1. Sentences where the word appears in the passage (The sentences can be the same for different words.), 
              2. Word, 
              3. Reading in Hiragana, 
              4. Part of Speech, 
              5. Definition, 
              6. More example sentences that are different from the passage. 
            Make sure the words in each line are not the same and there are 10 words in total.
            Do not provide any other words, just provide a JSON array.
        """
    all_messages = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=all_messages
    )
    vocabs = response.choices[0].message.content
    voc = json.loads(vocabs)
    vocabs_df = pd.DataFrame(voc)
    st.table(vocabs_df)


st.title(":violet[Yomou] - A Japanese Reading Assistant")

st.markdown('''This website is designed to assist you in learning Japanese. 
            You can use this website to translate Japanese paragraphs into English and learn new Japanese words''')

    
input = st.text_area("Enter a Japanese paragraph", "Type your paragraph here...")


if st.button("Translate"):
    translate()

if st.button("Get Vocabularies"):
    get_vocabs()