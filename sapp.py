import streamlit as st
from utils import generate_script
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchRun

def generate_script(prompt, video_length, creativity, api_key):

    # Template for generating title
    title_template = PromptTemplate(
        input_variable = ['subject'],
        template = 'please come up with a title for a Youtube video on {subject}'
    )

    # Template to generating the video script using search engine 
    script_template = PromptTemplate(
        input_variables = ['title', 'DuckDuckGO_Search', 'duration'],
        template = 'Create a script for a youtube Video based on the title for me. TITLE: {title} of duration: {duration} minutes using using this search data {DuckDuckGo_Search}'
    )

    # setting uo the OpenAl
    llm = OpenAI(temperature = creativity,  openai_api_key = api_key, model_name = 'gpt-3.5-turbo-instruct')

    # Create chain for the Title & Video Script

    title_chain = LLMChain(llm = llm, prompt = title_template, verbose = True)
    script_chain = LLMChain(llm = llm, prompt = script_template, verbose = True)

    # creating the search Engine
    search = DuckDuckGoSearchRun()

    # Executing the chain we created for title
    title = title_chain.run(prompt)

    # Executing the chain we created for Script by taking help of search engine 
    search_result = search.run(prompt)
    script = script_chain.run(title = title, DuckDuckGo_Search = search_result, duration = video_length)

    # Returning the Output
    return search_result, title, script


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
