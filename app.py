from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
import os
from langchain.agents import tool
import requests
import urllib.parse

import warnings

warnings.filterwarnings("ignore")


os.environ["GROQ_API_KEY"] = "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"

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")


chat_history = []  # Use a list to store messages

# Set an initial system message (optional)
system_message = SystemMessage(content="You are an industry expert in the filed of mobile phones. give answer in a short and meaningful way.")
chat_history.append(system_message)

# Chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))  # Add user message

    # Get AI response using history
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))  # Add AI message

    print(f"AI: {response}")


print("---- Message History ----")
print(chat_history)