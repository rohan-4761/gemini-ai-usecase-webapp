import streamlit as st
from streamlit_option_menu import option_menu
import os
from PIL import Image

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)

# dynamic path
working_directory = os.path.dirname(os.path.abspath(__file__))

# setting up the page configuration

st.set_page_config(
    page_title="Gemini_AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:

    selected = option_menu("Gemini AI",
                           ["Chatbot",
                               "Image Captioning",
                               "Embed Text",
                               "Ask me anything"
                           ],
                           menu_icon='robot',
                           icons=["chat-dots-fill",
                                  "image-fill",
                                  "textarea-t",
                                  "patch-question-fill"],
                           default_index=0
                           )


# function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


if selected == 'Chatbot':
    model = load_gemini_pro_model()

    # initialize the chat session in streamlit if not already exist
    if 'chat-session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 Chatbot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

#     input field
    user_prompt = st.chat_input("Ask Gemini-Pro... ")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

if selected == 'Image Captioning':
    st.title("📸 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "Write a short caption for this image"
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

if selected == 'Embed Text':
    st.title("🔠 Embed Text")

    input_text = st.text_area(label='', placeholder="Enter the text to get the embeddings.")

    if st.button("Get Embedding"):
        gemini_response = embedding_model_response(input_text)
        st.markdown(gemini_response)

if selected == 'Ask me anything':
    st.title("🙋‍♂️ Ask me a Question.")

    user_prompt = st.text_area(label='', placeholder="Ask Gemini-Pro...")

    if st.button("Get response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
