from dotenv import load_dotenv
import os
import requests
import chainlit as cl
from agents import Agent, Runner, tool, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunConfig
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

# ✅ Tool 1: Add two numbers
@function_tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b

# ✅ Tool 2: Multiply two numbers
@function_tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b


# ✅ Tool 3: Fetch weather for a city
@function_tool
def get_weather(city: str) -> str:
    """Returns current temperature and weather condition for a city."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    response = requests.get(url)
    data = response.json()

    if "error" in data:
        return f"❌ Could not find weather for '{city}'."

    temp_c = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    return f"The current temperature in {city} is {temp_c}°C with {condition.lower()}."


# ✅ On chat start
@cl.on_chat_start
async def on_chat_start():
    agent = Agent(
        name="Multi-Tool Agent",
        instructions="""
        You are a smart assistant that can either:
        - Add two numbers using the 'add' tool.
        - Muliply two numbers using the 'multiply' tool.
        - Tell the weather of a city using the 'get_weather' tool.

        Do not guess answers. Always use the appropriate tool for math or weather queries.
        """,
        model=model,
        tools=[add, multiply, get_weather]
    )

    cl.user_session.set("agent", agent)
    await cl.Message(content="👋 Hello! I'm a Multi Agent. I can answer math questions as well as tell you the weather.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    msg = cl.Message(content="🔍 Let me figure that out...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))  
    response = await Runner.run(agent, message.content)

    await cl.Message(content=response.final_output).send()
