from streamlit_option_menu import option_menu
from PIL import Image
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def gemini_pro():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        system_instruction="You're a Yoruba Teacher named Patrick. You're 30 years old. Personify this character without ever mentioning that you're an AI.",
    )
    return model

def gemini_img(model, prompt, image):
    response = model.generate_content([prompt, image])
    return response.text
# Set page title and icon
st.set_page_config(
    page_title="Patrick Yoruba Language Teacher",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "Google Gemini AI",
        ["PatrickChat", "Asking Through Images"],
        menu_icon="robot",
        icons = ["chat-dots-fill", "image-fill"],
        default_index=0
    )

def roleForStreamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

if user_picked == 'PatrickChat':
    model = gemini_pro()
    
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = model.start_chat(history=[])

    st.title("Patrick Chat Session")

    #Display the chat history
    for message in st.session_state.chat_history.history:
        with st.chat_message(roleForStreamlit(message.role)):    
            st.markdown(message.parts[0].text)

    # Get user input
    user_input = st.chat_input("Message TalkBot:")
    if user_input:
        st.chat_message("user").markdown(user_input)
        reponse = st.session_state.chat_history.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(reponse.text)

if user_picked == 'Asking Through Images':
    model = gemini_pro()

    st.title("Asking Through Images...")

    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    user_prompt = st.text_input("Enter the prompt for image captioning:")

    if st.button("Generate Caption"):
        load_image = Image.open(image)

        colLeft, colRight = st.columns(2)

        with colLeft:
            st.image(load_image.resize((800, 500)))

        caption_response = gemini_img(model, user_prompt, load_image)

        with colRight:
            st.info(caption_response)