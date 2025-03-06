from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os

import warnings

warnings.filterwarnings("ignore")


os.environ["GROQ_API_KEY"] = "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"

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")


chat_history = []  # Use a list to store messages

# Set an initial system message (optional)
system_message = SystemMessage(content="You are an industry expert in the filed of mobile phones. give answer in a short and meaningful way. If the question is not related to mobile, answer as I don't have taht knowledge except mobile and technology")
chat_history.append(system_message)


while True:
    query = input("You (for exit type 'exit'): ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    # Get AI response using history
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    print(f"AI: {response}")

