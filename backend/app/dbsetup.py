import asyncpg, asyncio
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

async def create_table_if_not_exists(pool):
    async with pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS logs_vector (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    page_content TEXT,
                    embedding VECTOR(3072)
                )
                """
            )
    print("Table created or already exists.")

async def insert_document(pool, doc):
    async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO logs_vector (source, page_content, embedding)
                VALUES ($1, $2, $3)
                """,
                doc['source'], doc['content'], str(doc['embedding'])
            )

async def load_and_insert_documents(pool, file_path):
    loader = CSVLoader(file_path=file_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, separators=["\n\n", "\n", " ", ""])
    all_splits = text_splitter.split_documents(data)

    embeddings = OllamaEmbeddings(model="llama3.2")

    for split in all_splits:
        embedding = embeddings.embed_query(split.page_content)
        doc = {
            "source": split.metadata.get('source', 'unknown'),
            "content": split.page_content,
            "embedding": embedding
        }
        await insert_document(pool, doc)
    print(f"Data from {file_path} inserted successfully.")

async def main():
    pool = await asyncpg.create_pool(
        host='',
        database='',
        user='',
        password=''
    )

    await create_table_if_not_exists(pool)
    print("Database setup completed.")

    files = [
        "./data/linux/Linux_2k.log_templates.csv", 
        "./data/apache/Apache_2k.log_templates.csv", 
        "./data/zoo-keeper/Zookeeper_2k.log_templates.csv"
    ]
    for file_path in files:
        await load_and_insert_documents(pool, file_path)
    print("Successfully inserted log embeddings")

    await pool.close()

asyncio.run(main())
