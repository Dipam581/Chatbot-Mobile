from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.agents import tool
import requests
import os
import urllib.parse
import warnings
warnings.filterwarnings("ignore")

os.environ["GROQ_API_KEY"] = "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"

# Initialize LLM
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

chat_history = []

# System Message
system_message = SystemMessage(
    content="You are an industry expert in mobile phones. Give short, meaningful responses. "
            "If the question is not related to mobiles or technology, answer as: 'I don't have that knowledge.'"
)
chat_history.append(system_message)


# Build dynamic url
def build_search_url(query, page=0, size=10, keep_casing=True):
    base_url = "https://api.techspecs.io/v5/products/search"
    params = {
        "query": query,
        "keepCasing": str(keep_casing).lower(),
        "page": page,
        "size": size
    }
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"


# API Tools
@tool
def get_all_mobile_data():
    """Returns all mobile brands and specifications."""
    url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/all-brands"
    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

@tool
def get_brands_data(brand: str = "Apple"):
    """Returns specific brand details and specifications."""
    url = f"https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-models-by-brandname/{brand}"
    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

@tool
def mobile_brand_data(query, page=0, size=10):
    """Fetch mobile brand details from TechSpecs API."""
    url = build_search_url(query, page, size)
    headers = {
        "accept": "application/json",
        "X-API-KEY": "81a8f2f6-dec3-4d15-96bc-6262e7469838",
        "X-API-ID": "67c6e3c2cae838e744780013"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# LangChain ReAct Agent Setup
llm = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")
tools = [get_all_mobile_data, get_brands_data, mobile_brand_data]

prompt_template = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Interactive Chat Loop
while True:
    query = input("You (type 'exit' to stop): ")
    if query.lower() == "exit":
        break
    
    chat_history.append(HumanMessage(content=query))

    if "phone" in query.lower() or "mobile" in query.lower() or "specification" in query.lower():
        response = agent_executor.invoke({"input": query})
    else:
        result = model.invoke(chat_history)
        response = result.content
        chat_history.append(AIMessage(content=response))

    print(f"AI: {response}")
