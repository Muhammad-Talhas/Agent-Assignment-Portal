from dotenv import load_dotenv
import os
import requests
import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunConfig
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
def get_weather(city: str) -> str:
    """Fetch current temperature for a given city."""
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"❌ Could not find weather for '{city}'."

        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        return f"The current temperature in {city} is {temp_c}°C with {condition.lower()}."

    except Exception as e:
        return f"❌ Failed to fetch weather: {str(e)}"

@cl.on_chat_start
async def on_chat_start():
    agent = Agent(
        name="Weather Info Agent",
        instructions="""
        You are a weather assistant. If the user asks for weather in any city, use the get_weather tool.
        You should not answer weather questions on your own—always call the tool.
        """,
        model=model,
        tools=[get_weather]
    )

    cl.user_session.set("agent", agent)

    await cl.Message(content="🌤️ Hello! I am a Weather Info Agent!\nWhich city's weather would you like to know? ").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    msg = cl.Message(content="🔍 Checking weather...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))  
    response = await Runner.run(agent, message.content)

    await cl.Message(content=response.final_output).send()
