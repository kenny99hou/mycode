# Import necessary libraries
from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# --- Configuration ---
# Ensure your OpenAI API key is set as an environment variable
# export OPENAI_API_KEY="your-api-key-here" 

app = FastAPI()

# Step 1: Initialize the Language Model (LLM)
# Using GPT-3.5-turbo as an example, suitable for customer service tasks
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# Step 2: Define the AI persona and task using a prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and polite AI customer service assistant for an electronics store. Your goal is to answer customer questions accurately and resolve their issues. If you don't know the answer, politely state that you cannot assist with that specific query and suggest they contact a human agent."),
    ("user", "{user_message}")
])

# Step 3: Chain the components together (LLMChain)
# This chain takes the user input, formats it into the prompt, sends to the LLM, and gets the text response.
chain = prompt_template | llm | StrOutputParser()

# Step 4: Create a simple API endpoint to interact with the assistant
@app.post("/support")
async def support(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    if not user_message:
        return {"error": "Message field is required."}

    # Invoke the chain to get the AI response
    ai_response = chain.invoke({"user_message": user_message})
    
    return {"reply": ai_response}

# To run this, save the file (e.g., `main.py`) and use Uvicorn:
# uvicorn main:app --reload
# You can then send a POST request to http://127.0.0.1:8000/support with a JSON body:
# {"message": "My order number 12345 hasn't arrived yet."}

