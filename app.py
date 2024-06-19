import streamlit as st
from utils import generate_script

# Applying Styling
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#FFFFFF;
    }
</style>""", unsafe_allow_html=True)

# Creating session state Variable

if 'API_KEY' not in st.session_state:
    st.session_state['API_KEY'] = ''

st.title('❤️ Youtube Scripting Writing AI')

# sidebar to capture the OpenAI API KEY

st.sidebar.title('😎🗝️')
st.session_state['API_KEY'] = st.sidebar.text_input('Enter your API KEY', type = 'password')
st.sidebar.image('Youtube.jpg', width = 300, use_column_width = True)

# Captures user inputs

prompt = st.text_input('Enter your Topic', key = 'prompt')
video_length = st.text_input('Expected Video Length')
creativity = st.slider('Words limit ⭐ - (0 Low || 1 HIGH)', 0.0, 1.0, 0.2, step = 0.1)

submit = st.button('Generate Script')

if submit:

    if st.session_state['API_KEY'] and prompt and video_length:
        search_result, title, script = generate_script(prompt, video_length, creativity, st.session_state['API_KEY'] )
        st.success('Hope you like this script ❤️')

        # Display Title
        st.subheader('Title:🔥')
        st.write(title)

        #Display video Script
        st.subheader('Your Video Script:📜')
        st.write(script)

        # Display Search Engine Result
        st.subheader('check out - DuckDuckGo Search: 🔍')
        with st.expander('show me 👀'):
            st.info(search_result)
    else:
        st.error('oooops!!! Please Provide API Key or Input the mandatory keyword')


