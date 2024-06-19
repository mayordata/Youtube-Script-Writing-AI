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




