import requests
import json
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

API_URL = "https://sdw-2023-prd.up.railway.app"


def get_users_ids_from_csv() -> list:
    users_csv = pd.read_csv("user_ids.csv")
    return users_csv["USER_ID"].to_list()

def get_user_data_from_api(id : int) -> dict:
    response = requests.get(f"{API_URL}/users/{id}")
    return response.json() if response.status_code == 200 else {"id": id, "status_code": response.status_code}

def generate_ai_mkt_message(users):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em marketing financeiro."
             },
            {
                "role": "user",
                "content": f"Escreva uma mensagem para o cliente {users['name']} sobre a importância de investir seu dinheiro. Máximo de 150 caracteres."
            }
        ]
    )
    return completion

load_dotenv()
# print(os.getenv("GPT_KEY"))

print(get_user_data_from_api(1))

