# 🧠 GenAI Prompt Engineering using LangChain

## 📌 Project Overview

This project is a **Mini Prompt Engine** built using LangChain that converts user input into **structured, dynamic prompts** instead of using hardcoded strings.

The goal of this project is to understand how real-world Generative AI systems handle prompts in a **modular, reusable, and scalable way**.

---

## 🎯 Objective

* Replace hardcoded prompts with **LangChain PromptTemplate**
* Build **dynamic prompt generation systems**
* Design a **complete prompt pipeline**
* Implement **input validation**
* Create reusable and flexible prompt structures

---

## 🛠️ Tech Stack

* Python
* LangChain
* Jupyter Notebook / Google Colab

---

## ⚙️ Project Pipeline

The system follows this flow:

User Input → Validation → Prompt Template → Dynamic Prompt Generation → Output

---

## 📂 Tasks Implemented

### ✅ Task 1: Replace Hardcoded Prompts

Converted static f-string prompts into reusable `PromptTemplate`.

---

### ✅ Task 2: Multi-Input Prompt System

Created a template with multiple inputs:

* topic
* audience
* tone

Example:
Explain AI for beginners in a friendly tone

---

### ✅ Task 3: Prompt Variations Engine

Built multiple templates for different use cases:

* Teaching → Step-by-step explanation
* Interview → Question generation
* Storytelling → Narrative explanation

---

### ✅ Task 4: ChatPromptTemplate System

Implemented chat-style prompts with roles:

* Teacher
* Interviewer
* Motivator

This simulates real conversational AI systems.

---

### ✅ Task 5: Input Validation Layer

Validated user inputs before generating prompts.

Rules:

* audience → beginner, intermediate, expert
* tone → formal, casual, fun

Invalid inputs are automatically handled with default values.

---

### ✅ Task 6: Prompt Generator Function

Created a reusable function:

generate_prompt(topic, audience, tone, style)

This function dynamically generates prompts based on user inputs.

---

### ✅ Task 7: Template Reusability Test

Tested one template with multiple inputs to ensure:

* Same structure
* Different outputs

---

## 🚀 How to Run the Project

1. Install dependencies:

```bash
pip install langchain langchain-core
```

2. Run the notebook:

* Open in Jupyter Notebook or Google Colab
* Execute cells step by step

---

## 📌 Example Output

INPUT:
topic = Python
audience = beginner
tone = fun
style = teaching

OUTPUT:
Explain Python for beginner in a fun teaching style

---

## ⚠️ Important Notes

* No f-strings are used ❌
* PromptTemplate is used everywhere ✅
* Code is modular and reusable ✅
* Logic is separated from templates ✅

---

## 🧠 Key Learnings

* How to design **prompt pipelines** instead of static prompts
* Importance of **reusability in AI systems**
* Handling **multiple inputs dynamically**
* Using LangChain for **structured prompt engineering**

---

## 🔮 Future Improvements

* Integrate with LLM APIs (OpenAI, Hugging Face)
* Build a UI using Streamlit
* Add more advanced prompt styles
* Create real-world chatbot applications

---

## 📎 Author

Kiran Raj

---

## ⭐ Final Insight

This project demonstrates a shift from simply writing prompts to **engineering prompt systems**, which is a critical skill in modern Generative AI development.
