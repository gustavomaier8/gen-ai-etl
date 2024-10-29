import requests
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
API_URL = os.getenv("API_URL")
API_AI_KEY = os.getenv("API_AI_KEY")


def get_users_ids_from_csv() -> list:
    """
    Lê o arquivo CSV contendo IDs de usuários e retorna uma lista com esses IDs.

    Returns:
        list: Lista contendo IDs de usuários (USER_ID) presentes no arquivo user_ids.csv.
    """

    users_csv = pd.read_csv("gen-ai-etl\\user_ids.csv")
    return users_csv["USER_ID"].to_list()

def get_user_data_from_api(id : int) -> dict:
    """
    Busca os dados de um usuário específico na API usando seu ID.

    Args:
        id (int): ID do usuário a ser buscado.

    Returns:
        dict: Dados do usuário retornados pela API.
    """
        
    response = requests.get(f"{API_URL}/users/{id}")
    return response.json() if response.status_code == 200 else print(f"Erro ao extrair os dados do usuário de ID {id} da API. Error code: {response.status_code}")

def generate_ai_mkt_message(user_data : dict) -> str:
    """
    Gera uma mensagem de marketing personalizada para um usuário específico utilizando a API de IA.

    Args:
        user_data (dict): Dados do usuário.

    Returns:
        dict: Dados do usuário atualizados com a nova mensagem de marketing gerada.
    """

    genai.configure(api_key=API_AI_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Você é um especialista em marketing financeiro. Escreva uma mensagem para o cliente {user_data['name']} sobre a importância de investir seu dinheiro. Máximo de 150 caracteres.")
    
    user_data["news"].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": response.text
        })
    
    return user_data

def update_user_on_api(user_data : dict) -> bool:
    """
    Atualiza os dados de um usuário na API com as novas informações.

    Args:
        user_data (dict): Dados do usuário, incluindo a nova mensagem de marketing gerada.

    Returns:
        bool: Retorna True se a atualização foi bem-sucedida, False caso contrário.
    """

    response = requests.put(f"{API_URL}/users/{user_data['id']}", json=user_data)
    return True if response.status_code == 200 else False

def main():
    """
    Função principal que executa o processo completo de:
    - Carregar IDs dos usuários do CSV.
    - Buscar dados de cada usuário na API.
    - Gerar e atualizar a mensagem de marketing personalizada para cada usuário.
    """

    users_ids = get_users_ids_from_csv()

    for user_id in users_ids:
        user_data = get_user_data_from_api(user_id)
            
        if user_data:
            updated_user_data = generate_ai_mkt_message(user_data)
            is_updated = update_user_on_api(updated_user_data)
            print(f"Usuário {user_data['name']} atualizado com sucesso!") if is_updated else print(f"Usuário {user_data['name']} não foi atualizado. Verificar!")


if __name__ == "__main__":
    main()