# 🧮 Assignment 2: Math Function Tool Agent

This assignment demonstrates how to build a simple math assistant agent using the **OpenAI Agent SDK** and **Chainlit**. The agent is capable of solving basic math problems such as addition and multiplication by using Python functions registered as tools.

---

## 🎯 Objective

Create an AI agent that can:

- Interpret natural language math questions.
- Decide when to use a tool (e.g., `add`, `multiply`) to answer.
- Return the computed result as a natural response.

---

## 🛠️ Tools Used

### Built-in Tools:
- `add(a: int, b: int)` → Adds two numbers.
- `multiply(a: int, b: int)` → Multiplies two numbers.

---

## 🧪 Example Questions

Try these after running the agent:

- What is 5 + 7?
- Multiply 6 and 9.
- Add 45 and 15.
- What is the result of 3 times 8?

---

## 📸 Screenshots

### ➤ Example 1: Addition
![Addition Example](screenshots/chat-1.png)

### ➤ Example 2: Multiplication
![Multiplication Example](screenshots/chat-2.png)

## 🚀 How to Run

Make sure you have a valid `.env` file with your `GEMINI_API_KEY`.

### Step 1: Install dependencies
```bash
uv pip install -r requirements.txt  # Or manually install chainlit + SDK
