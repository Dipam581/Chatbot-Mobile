from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
import datetime
import getpass
import os
from langchain.agents import tool
import requests
import urllib.parse

os.environ["GROQ_API_KEY"] = "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"


def build_search_url(query, page=0, size=10, keep_casing=True):
    base_url = "https://api.techspecs.io/v5/products/search"
    params = {
        "query": query,
        "keepCasing": str(keep_casing).lower(),  # convert boolean to 'true'/'false'
        "page": page,
        "size": size
    }
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"

# Example usage:
dynamic_url = build_search_url("iPhone 14", page=0, size=10)


@tool
def mobile_brand_data(query, page=0, size=10):
    """ Return the brand details of the mobile """
    url = build_search_url(query, page, size)
    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "X-API-KEY": "81a8f2f6-dec3-4d15-96bc-6262e7469838",
        "X-API-ID": "67c6e3c2cae838e744780013"
    }

    response = requests.get(url, headers=headers)


@tool
def mobile_specific_data():
    """ Return the specific mobile brand details """
    url = "https://api.techspecs.io/v5/products/63e96260ff7af4b68a304765?lang=en"

    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "X-API-KEY": "81a8f2f6-dec3-4d15-96bc-6262e7469838",
        "X-API-ID": "67c6e3c2cae838e744780013"
    }

    response = requests.get(url, headers=headers)

@tool
def get_all_mobile_data():
    """ Returns all types of brands mobile data """

    url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/all-brands"

    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    return response.json()

@tool
def get_brands_data(brand: str = "Apple"):
    """ Returns specific brand of mobile data and its specifications """

    url = f"https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-models-by-brandname/{brand}"

    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()


llm = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")



query = "Which varient should I buy from samsung on 2025?"

prompt_template = hub.pull("hwchase17/react")

tools = [get_all_mobile_data, get_brands_data]  #mobile_brand_data, mobile_specific_data

agent = create_react_agent(llm, tools, prompt_template)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": query})