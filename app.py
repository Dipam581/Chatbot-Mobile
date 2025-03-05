from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
import os
from langchain.agents import tool
import requests
import urllib.parse

os.environ["GROQ_API_KEY"] = "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"


def build_mobile_spec_url(brand: str, model: str):
    encoded_model = urllib.parse.quote(model)
    base_url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-specifications-by-brandname-modelname"

    url = f"{base_url}/{brand}/{encoded_model}"
    return url


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
def get_model_device_data(brands):
    """ Returns specific details about mobile brand and model """
    arguments = brands["brand"].split(",")
    brand = arguments[0].strip()
    model = arguments[1].strip()
    
    url = build_mobile_spec_url(brand, model)
    # url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-specifications-by-brandname-modelname/Samsung/Galaxy%20S22%20Ultra%205G"

    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }
    model_list = []
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for mod in data:
        if (mod != "phoneDetails" or mod != "gsmTestsDetails" or mod != "gsmPlatformDetails" or mod != "gsmNetworkDetails"):
            model_list.append(data[mod])
    return model_list
        

@tool
def get_all_mobile_data():
    """ Returns all types of brands mobile data """

    url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/all-brands"

    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }
    product_list = []
    response = requests.get(url, headers=headers)
    
    for pro in response.json():
        product_list.append(pro["brandValue"].lower())
        
    return product_list

@tool
def get_brands_data(brand: str = "Apple"):
    """ Returns specific brand of mobile data and its specifications """

    url = f"https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-models-by-brandname/{brand}"

    headers = {
        "x-rapidapi-key": "517b6a7ccdmsh09b724099070929p1709a0jsn337969857059",
        "x-rapidapi-host": "mobile-phone-specs-database.p.rapidapi.com"
    }

    brand_model_list = []
    response = requests.get(url, headers=headers)
    
    for brand in response.json():
        brand_model_list.append(brand["modelValue"].lower())
        
    return brand_model_list


llm = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")



query = "Which phones are best in terms of battery and suggest me which one should I buy with a budget of 50000 indian rupees?"

prompt_template = hub.pull("hwchase17/react")

tools = [get_all_mobile_data, get_brands_data, get_model_device_data] 

agent = create_react_agent(llm, tools, prompt_template)

agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)

ag = agent_executor.invoke({"input": query})
print(ag["output"])