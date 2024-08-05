from langchain_community.llms import Ollama
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import PyMuPDFLoader
import chainlit as cl
from datetime import datetime
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema import StrOutputParser

def set_custom_prompt():
    ## Prompt construction
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a travel Chat Assistant. Your job is to only answer travel questions and make travel plans and recommendations based on things-to-do of high rankings in tripadvisor.com.  Do not answer other questions",
            ),
            ("human", "{question}"),
        ]
    )
    
    return prompt

def load_llm():
    # LLM
    llm = Ollama(model="phi3", verbose=True)
    print(f"Loaded LLM model {llm.model}")
    return llm

# chainlit code
@cl.on_chat_start
async def start():
    elements = [cl.Image(name="image1", display="inline", path="assets/bot.jpg")]
    msg = cl.Message(content="I am a travel virtual assitant II. How can I help you?", elements=elements)
    await msg.send()

    model = load_llm()
    prompt = set_custom_prompt()
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)
    
@cl.on_message
async def main(message: cl.Message):
    start_time = datetime.now()
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
   
    end_time = datetime.now()
    time_taken = end_time - start_time
    print("total time taken was:", time_taken)
    
   