import requests

BASE_URL = "http://127.0.0.1:1000/api/"

def api_request(method, endpoint, token=None, data=None):
    """
    Função para fazer requisições HTTP a API.
    
    Args:
        method (str): Método HTTP (GET, POST, etc.).
        endpoint (str): Endpoint da API.
        token (str, optional): Token de autenticação, se necessário.
        data (dict, optional): Dados JSON a serem enviados na requisição.

    Returns:
        dict: Resposta da API em formato JSON.
    """
    url = f"{BASE_URL}{endpoint}"
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.request(method, url, headers=headers, json=data)
    return response


