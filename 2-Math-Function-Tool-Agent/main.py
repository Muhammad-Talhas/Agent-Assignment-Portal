from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI, RunConfig
import os
import asyncio
import chainlit as cl
from agents.tool import function_tool
from typing import cast

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

@function_tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@function_tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

@cl.on_chat_start
async def on_chat_start():
    agent = Agent(
        name="Math Tool Agent",
        instructions="""
        You are a helpful math assistant. Use the available tools to solve simple math problems like addition and multiplication.
        Do not try to solve math yourself; instead, always use the registered tools (add or multiply).
        Only answer math-related questions.
        """,
        model=model,
        tools=[add, multiply],
    )

    cl.user_session.set("agent", agent)

    await cl.Message(content="🤖 Welcome to the Math Function Tool Agent!\nYou can ask me basic math questions").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    msg = cl.Message(content="🤔 Let me calculate that...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))  
    response = await Runner.run(agent, message.content)

    await cl.Message(content=response.final_output).send()
