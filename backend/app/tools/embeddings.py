from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS 

embeddings = OllamaEmbeddings(
    model="llama3.2",
)

def retrieve_apache_embeddings(level:str, content : str):     

    vectorstore = FAISS.load_local("apache_vector_store", embeddings, allow_dangerous_deserialization=True)
    print("inside event", level, content)
    query = f'''
    Retrieve Event Id and Event Template from this error log 
    {level} {content}
    '''

    docs = vectorstore.similarity_search_with_relevance_scores(query,fetch_k=4)

    return [ docs[0][0].page_content , level , content]

def retrieve_zookeeper_embeddings(level:str, component:str, content : str):     

    vectorstore = FAISS.load_local("zookeeper_vector_store", embeddings, allow_dangerous_deserialization=True)
    print("inside event", level, content)
    query = f'''
    Retrieve Event Id and Event Template from this error log 
    {level} {component} {content}
    '''

    docs = vectorstore.similarity_search_with_relevance_scores(query,fetch_k=4)

    return [ docs[0][0].page_content , level , content]


def retrieve_linux_embeddings(level:str, component:str, content : str):     

    vectorstore = FAISS.load_local("linux_vector_store", embeddings, allow_dangerous_deserialization=True)
    print("inside event", level, content)
    query = f'''
    Retrieve Event Id and Event Template from this error log 
    {level} {component} {content}
    '''

    docs = vectorstore.similarity_search_with_relevance_scores(query,fetch_k=4)

    return [ docs[0][0].page_content , level , content]
 