from fastapi import FastAPI
from utils import json_to_dict_list
import os
from typing import Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
path_to_json = os.path.join(parent_dir, 'game-shop.json')


app = FastAPI()


@app.get("/customers")
def get_all_customers():
    return json_to_dict_list(path_to_json)

@app.get("/")
def home_page():
    return {"message": "Hello World!"}

@app.get("/customers/{customer_id}")
def get_all_customers_customer_id(customer_id: int):
    customers = json_to_dict_list(path_to_json)
    return_list = []
    for student in customers:
        if student["customer_id"] == customer_id:
            return_list.append(student)
    return return_list