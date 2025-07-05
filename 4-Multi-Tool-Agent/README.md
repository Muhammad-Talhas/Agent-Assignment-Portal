# 🧠 Assignment 4: Agent with Multiple Tools

This project showcases an AI agent capable of answering **both math and weather questions** using separate tools, built using the **OpenAI Agent SDK** and **Chainlit**.

---

## 🎯 Objective

Build an AI agent that:

- Uses the `add(a, b)` and `multiply(a, b)` tools for math questions.
- Uses the `get_weather(city)` tool to fetch weather data.
- Automatically selects the appropriate tool based on the user’s input.

---

## 🔧 Tools Used

### 1. Math Tools

```python
@function_tool
def add(a: int, b: int) -> int:
    return a + b

@function_tool
def multiply(a: int, b: int) -> int:
    return a * b


### 2. Weather Tools
@function_tool
def get_weather(city: str) -> str:
    # Returns current temperature and weather condition using WeatherAPI
