import requests
from requests.exceptions import HTTPError

API_KEY = "5RSj7iUp2oegnb9pbRl3nahHjYW3KDNhgideK4XDkUqliWHdgD"
BASE_URL = "http://localhost:9283"

headers = {"GROCY-API-KEY":API_KEY,
            "Accept": "application/json",
            "Content-Type":"application/json"
           }

our_data = {}

def is_product_exists(product:str) -> int:
    try:
        response = requests.get(f"{BASE_URL}/api/objects/products",headers= headers)
        response.raise_for_status()
        response_json = response.json()
        for data in response_json:
            id = data["id"]
            name = data["name"]
            if name == product:
                return id
        return -1
    except HTTPError as http_err :
            print(f"HTTP error occurred: {http_err}")
            return -1
    except Exception as err:
            print(f"Ann error occurred: {err}")
            return -1    
        


#quantity_id 2->piece, 3->pack
#location_id 2->fridge, 3->pantry
def creating_product(name:str, location_id:int,quantity_id:int )-> int:
     try:
          product = {
                        "name": name,
                        "location_id":location_id,
                        "qu_id_purchase": quantity_id,
                        "qu_id_stock":quantity_id
                    }
          
          response = requests.post(f"{BASE_URL}/api/objects/products",headers=headers,json= product)
          response.raise_for_status()        
          return response.status_code

     except HTTPError as http_err :
          print(f"HTTP error occurred: {http_err}")
          return -1
     
     except Exception as err:
          print(f"Ann error occurred: {err}")
          return -1
          
#Best before date format is yyyy-mm-dd
def adding_product_to_stock(product:str, amount:int, best_before_date:str) ->str:
     #This part is for getting the product_id from db
     try:
        response = requests.get(f"{BASE_URL}/api/objects/products",headers= headers)
        response.raise_for_status()
        response_json = response.json()
        product_id = None
        for data in response_json:
            id = data["id"]
            name = data["name"]
            if name == product:
                product_id = id
                break
        if product_id is None:
             return f"Product '{product}' not found."
             
        #This part is actual part where we write it to db
        product_to_write = {
                "amount": amount,
                "best_before_date": best_before_date,
                "transaction_type":"purchase"
        }

        response = requests.post(f"{BASE_URL}/api/stock/products/{product_id}/add"
                                 ,headers=headers,json= product_to_write)
        
        response.raise_for_status()    
        return f"Added {product} to stock succesfully"
                       
     except HTTPError as http_err :
        return f"HTTP error occurred: {http_err}"
     
     except Exception as err:
          return f"An error occured f{err}"
    

def product_consuming(product: str, amount: int) -> str:
    try:
        response = requests.get(f"{BASE_URL}/api/objects/products", headers=headers)
        response.raise_for_status()
        products = response.json()

        product_id = None
        for p in products:
            if p["name"] == product:
                product_id = p["id"]
                break

        if not product_id:
            return f"Product '{product}' not found."

        consume_data = {"amount": amount, "transaction_type": "consume"}

        response = requests.post(f"{BASE_URL}/api/stock/products/{product_id}/consume",
                                 headers=headers, json=consume_data)

        if response.status_code == 200:
            return f"Successfully consumed {amount} of {product}."
        return f"Failed to consume product '{product}'. Status Code: {response.status_code}"

    except Exception as err:
        return f"An error occurred: {err}"


creating_product('pineaple', 2, 2)
adding_product_to_stock('pineaple',31,'2025-08-21')
product_consuming('pineaple',1)

