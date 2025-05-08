'''
API_KEY is the key that is used to authenticate the requests to the Grocy API.
BASE_URL is the base URL of the Grocy API.

headers is a dictionary that contains the API key and the content type for the requests.
'''

import requests
from requests.exceptions import HTTPError\

API_KEY = "5RSj7iUp2oegnb9pbRl3nahHjYW3KDNhgideK4XDkUqliWHdgD"
BASE_URL = "http://localhost:9283"

headers = {"GROCY-API-KEY":API_KEY,
            "Accept": "application/json",
            "Content-Type":"application/json"
           }

our_data = {}

def is_product_exists(product:str) -> int:

    """
    Sends a GET request to the Grocy API to check if a product exists in the database.

    Returns the ID of the product if it exists, otherwise returns -1.

    Args:
       product_name (str): The name of the product to check.

    Returns:
       int: The ID of the product if it exists, otherwise -1.

    The function loops through the products in the database and checks if the given product exists.
    If found, it returns the product's ID.
"""

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
     '''
     Creates a new product in the Grocy Database.
        Args:
            name (str): The name of the product.
            location_id (int): The ID of the location where the product is stored.
            quantity_id (int): The ID of the quantity type for the product.

        Returns:
            int: The status code of the response from the API.
        The function checks if the product already exists in the database.
        If it does, it returns -1.
        If it doesn't, it creates a new product with the given name, location ID, and quantity ID.
        If the product is created successfully, it returns the status code of the response.
     '''

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
     
     '''
     Adding declared product into stock.
        Args:
            product (str): The name of the product to be added.
            amount (int): The amount of the product to be added.    
            best_before_date (str): The best before date of the product in 'YYYY-MM-DD' format.

        Returns:
            str: A message indicating the result of the operation.

        The function first checks if the product exists in the database.
        If it does, it retrieves the product ID.        
        If the product ID is found, it creates a dictionary with the amount and best before date.
        Then, it sends a POST request to the Grocy API to add the product to stock.
        If the request is successful, it returns a success message.    

     '''
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

    '''
    Works as a stock amount updater.
    if product amount is less than previous amount, it will consume the product.
    Args:
        product (str): The name of the product to be consumed.
        amount (int): The amount of the product to be consumed.
    Returns:
        str: A message indicating the result of the operation.
    The function first checks if the product exists in the database.
    If it does, it retrieves the product ID.
    If the product ID is found, it creates a dictionary with the amount and transaction type.
    Then, it sends a POST request to the Grocy API to consume the product.
    If the request is successful, it returns a success message.

    
    '''

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
