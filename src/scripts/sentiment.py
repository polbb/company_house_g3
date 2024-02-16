from helper_functions import wait_on_run, display_thread_messages, create_thread_message_lists
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os


# # initialize client
# load_dotenv('./.env.txt')

# # initialize client
# openai_key = os.environ.get('openai') # same as os.getenv('openai)
# client = OpenAI(api_key=openai_key)


# BELOW IS FOR STREAMLIT DEPLOYMENT
client = OpenAI(api_key=st.secrets.openai)


# @st.cache_data
def sentiment_analysis():

    thread = client.beta.threads.create()
    thread.id


    message_content = (
        f'Go through the text file "file-VZef3gDeVy4Wg3H4vo8AiSLJ" and understand it contents. '
        f'The text is a strategic report part of a financial statement. '
        f'Do a sentiment analysis. '
        'Start with a summary of the overall sentiment. '
        'You can expand with specifics after the summary. '
        'Be brief. '
        f'Output your sentiment analysis as response. '

    )

    message = client.beta.threads.messages.create(
        thread_id= thread.id,
        role= 'user',
        content= message_content,
        file_ids=['file-VZef3gDeVy4Wg3H4vo8AiSLJ'], 
    )

    instructions = (
        'You are an expert as both, underwriter and financial analyst. '
        'Your task is to examine a text and core the overall sentiment. '
        'You will be given a file id to the file. '
    )


    # update the description and load assistnt object
    assistant = client.beta.assistants.update(
        assistant_id='asst_FJ8OOlzHydbdUuPzCrVkMSsC',
        instructions=instructions
    )
    assistant.id


    run = client.beta.threads.runs.create(
        assistant_id= assistant.id,
        thread_id= thread.id,
    )

    with st.spinner('Analysis by ArgoX.ai ...'):
        wait_on_run(client=client, run=run, thread=thread)

    messages = client.beta.threads.messages.list(
        thread_id= thread.id,
        # order='asc'
    )

    display_thread_messages(messages)

    # # create a list of messages that can be used to write a log
    # messages_list = create_thread_message_lists(messages)

    response = messages.data[0].content[0].text.value

    return response