import requests
import urllib


def build_mobile_spec_url(brand: str, model: str):
    encoded_model = urllib.parse.quote(model)
    base_url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-specifications-by-brandname-modelname"

    url = f"{base_url}/{brand}/{encoded_model}"
    return url

# Example usage:

def get_model_device_data():
    """ Returns all types of brands mobile data """
    brand = "Samsung"
    model = "Galaxy S22 Ultra 5G"
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
    print(model_list)
        
get_model_device_data()