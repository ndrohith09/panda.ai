from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS 
import requests

embeddings = OllamaEmbeddings(
    model="llama3.2",
)


def retrieve_apache_embeddings(level: str, content: str):
    response = requests.get(
        "http://localhost:4195/search",
        params={"query": f"{level} {content}", "source": "./data/apache/Apache_2k.log_templates.csv"},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        result = data.get("response", [])
        return [result[0], level, content] if result else ["No results found", level, content]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ["Error retrieving data", level, content]


def retrieve_zookeeper_embeddings(level:str, component:str, content : str):     
    response = requests.get(
        "http://localhost:4195/search",
        params={"query": f"{level} {component} {content}", "source": "./data/zoo-keeper/Zookeeper_2k.log_templates.csv"},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        result = data.get("response", [])
        return [result[0], level, content] if result else ["No results found", level, content]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ["Error retrieving data", level, content]


def retrieve_linux_embeddings(level:str, component:str, content : str):     
    response = requests.get(
        "http://localhost:4195/search",
        params={"query": f"{level} {component} {content}", "source": "./data/linux/Linux_2k.log_templates.csv"},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        result = data.get("response", [])
        return [result[0], level, content] if result else ["No results found", level, content]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ["Error retrieving data", level, content]
 