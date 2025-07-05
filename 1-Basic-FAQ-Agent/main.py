from dotenv import load_dotenv
import os
import asyncio
import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunConfig

load_dotenv()
set_tracing_disabled(True)

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider
)

faq_agent = Agent(
    name="Basic FAQ Agent",
    instructions="""
You are a helpful FAQ chatbot. You must only answer a limited set of predefined questions. 
Here are the only questions you are allowed to answer, along with how you should respond:

1. Q: What is your name?  
   A: I am the Basic FAQ Agent.

2. Q: What can you do?  
   A: I can answer frequently asked questions about myself and how I work.

3. Q: Who created you?  
   A: I was created by a Talha Mehtab.

4. Q: How do you work?  
   A: I use AI technology to understand and respond to predefined questions.

5. Q: Where are you deployed?  
   A: I am running inside a Python application using Chainlit.

If any other question is asked, politely reply:  
"I'm sorry, I can only answer specific frequently asked questions."

Always be friendly and concise in your responses.
""",
    model=model,
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="🤖 Welcome to the Basic FAQ Bot! Ask me something.").send()

@cl.on_message
async def on_message(message: cl.Message):
    response = await Runner.run(faq_agent, message.content)
    await cl.Message(content=response.final_output).send()